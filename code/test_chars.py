import time
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from data import send_rooms_data, send_timetable_data_chars

# веса доп условий, по которым проводится подсчет качества постановок
WINDOWS_VALUE = 1
CORPUS_VALUE = 2


# проверка окон у преподов
def windows_check(timetable_data, teacher, time_slot, day_of_week):
	res = 0
	for group in timetable_data.keys():
		if (timetable_data[group][day_of_week][(time_slot % 10)+1][3] == teacher
			or timetable_data[group][day_of_week][(time_slot % 10)-1][3] == teacher) \
			and timetable_data[group][day_of_week][(time_slot % 10)][3] != teacher:
			res = 1

	return res


# проверка на наличие переходов между корпусами в перерыве
def corpus_check(timetable_data, room, time_slot, group, day_of_week):
	if (timetable_data[group][day_of_week][(time_slot % 10)+1][5]) % 10 == room % 10 \
		or (timetable_data[group][day_of_week][(time_slot % 10)-1][5]) % 10 == room % 10:
		return 1
	else:
		return 0


# функция генерирует словарь (ключ - отобранный тайм слот,
# значение - все возможные аудитории по конкретоному требованию)
def dict_generator(available_time, requirement, rooms_data):
	# d - словарь мэтчей аудиторий и времени
	d = {}
	for available_time_slot in available_time:
		d[available_time_slot] = []

	for req in rooms_data.keys():
		if req == requirement:
			for time_key in d.keys():
				time_slot = time_key
				d[time_slot].extend(rooms_data[req][time_slot])

	return d


def quality_check(time_rooms_match, timetable_data, teacher, group):
	max_quality = -1
	max_quality_time_room = []
	# полный перебор на неделю по всем возможным парам время - аудитория
	for day_of_week in timetable_data[group].keys():
		for time_slot in time_rooms_match.keys():
			if day_of_week == time_slot // 10:
				for room in time_rooms_match[time_slot]:
					# вычисление качества
					windows_mark = WINDOWS_VALUE * windows_check(timetable_data, teacher, time_slot, day_of_week)
					corpus_mark = CORPUS_VALUE * corpus_check(timetable_data, room, time_slot, group, day_of_week)

					quality = windows_mark + corpus_mark

					# определение максимального качества
					if quality > max_quality:
						max_quality = quality
						max_quality_time_room = [time_slot, room]

	return max_quality_time_room, max_quality


# ставит занятие в расписание
def lesson_filler(timetable_data, lesson, max_quality_values, encoders_dict):
	new_lesson = []
	for index in range(len(lesson)):
		if not isinstance(lesson[index], str):
			new_lesson.append(decoder(encoders_dict[index], [lesson[index]-1])[0])
	new_lesson.append(lesson[-1])

	# здесь надо декодировать значения из таблицы
	if max_quality_values:
		# перезаписываем вместо пустых значений занятия (кроме аудитории) значения лучшего занятия
		# по индексам timetable_data: первый - группа, второй - день недели, третий - конкретный номер занятия,
		# дальше - просто срез (берем тольк группу, занятие, препода, требование)
		timetable_data[lesson[0]][max_quality_values[0] // 10][max_quality_values[0] % 10][0:4] = new_lesson[0:4]
		# перезаписываем вместо пустого значения аудитории значения лучшей аудитории
		timetable_data[lesson[0]][max_quality_values[0] // 10][max_quality_values[0] % 10][-1] = max_quality_values[1]

		return timetable_data

	return timetable_data


# убирает взятую аудиторию из списка всех возможных аудиторий
def dict_cleaner(rooms_data, requirement, max_quality_values):
	index_to_drop = rooms_data[requirement][max_quality_values[0]].index(max_quality_values[1])
	rooms_data[requirement][max_quality_values[0]].pop(index_to_drop)

	return rooms_data


# вывод готового дня
def output(timetable_data):
	# group_num - номер группы только для вывода, group - номер
	# конкретной группы для которой ставится занятие из main
	for group_num in timetable_data.keys():
		print('Группа: {}'.format(group_num))
		print('-' * 8)
		for day, value in timetable_data[group_num].items():
			print('День: {}'.format(day))
			print('-' * 20)
			for num_lesson in value:
				print(num_lesson, sep=' ')
			print('-' * 20)


# подсчет кол-ва пар поставленных в конкретный день
def count_lessons(timetable_data, group):
	count = 0
	count_arr = []
	for day_of_week in timetable_data[group].values():
		for i in range(1, len(day_of_week)-1):
			if day_of_week[i][5] != 0:
				count += 1
		count_arr.append(count)
		count = 0

	return count_arr


# проверка жестких ограничений
def checker(timetable_data, group):
	available_time = []
	for day_of_week in timetable_data[group].values():
		if count_lessons(timetable_data, group)[(day_of_week[1][4] // 10) - 1] != 0:
			for i in range(1, len(day_of_week) - 1):
				if (day_of_week[i][5] == 0 and day_of_week[i][4] != 0) \
						and (day_of_week[i - 1][5] != 0 or day_of_week[i + 1][5] != 0) \
						and count_lessons(timetable_data, group)[(day_of_week[1][4] // 10)-1] < 4:
					available_time.append(day_of_week[i][4])
		else:
			for i in range(1, len(day_of_week) - 1):
				available_time.append(day_of_week[i][4])

	return available_time


# функция постановки нескольких занятий из массива занятий - при возврате rooms_data вылетает по приколу
def lessons_cycle(lessons_arr, encoders_dict):
	rooms_data = send_rooms_data()
	timetable_data = send_timetable_data_chars()

	for index, lesson in enumerate(lessons_arr):
		teacher, group, requirement, available_time = data_preprocessing(lesson, timetable_data)
		print('Работаем с: {}, {}, {}'.format(group, requirement, teacher))
		if len(available_time) == 0:
			break
		else:
			time_rooms_match = dict_generator(available_time, requirement, rooms_data)
			max_quality_values, max_quality = quality_check(time_rooms_match, timetable_data, teacher, group)
			print('Лучшие время и аудитория для {} занятия: {}'.format(index + 1, max_quality_values))
			print('Возможные временные слоты: {}'.format(available_time))
			print('Максимальное качество: {}'.format(max_quality), '\n')
			rooms_data = dict_cleaner(rooms_data, requirement, max_quality_values)
			timetable_data = lesson_filler(timetable_data, lesson, max_quality_values, encoders_dict)
			time.sleep(0.5)

	return timetable_data, rooms_data


def encoder(data):
	encoders_dict = {}
	for column_num, column in enumerate(data[['group', 'lesson', 'requirement']]):
		enc = LabelEncoder()
		data[column] = enc.fit_transform(data[column])
		encoders_dict[column_num] = enc

	data[['group', 'lesson', 'requirement']] = data[['group', 'lesson', 'requirement']] + 1

	return data, encoders_dict


def decoder(exact_encoder, value):
	return exact_encoder.inverse_transform(value)


# обработка входных данных
def data_preprocessing(lesson, timetable_data):
	teacher = lesson[3]
	group = lesson[0]
	requirement = lesson[2]
	available_time = checker(timetable_data, group)

	return teacher, group, requirement, available_time


def main():
	excel_file = 'D:/#python/SchedulingClasses/data/то_что_отдадут.xlsx'
	data = pd.read_excel(excel_file)
	encoded_data, encoders_dict = encoder(data)
	final_timetable = lessons_cycle(encoded_data.values, encoders_dict)
	output(final_timetable[0])


if __name__ == '__main__':
	# надо сделать, чтобы этот файл как то подгружал пользователь
	main()


# ограничение на минимальное кол-во пар в дне пока непонятно как реализовать, так что отложим до лучших времен
# преподаватель, группа, предмет - это можно сделать руками - это просто проставляется самими преподами
# прокачать проверку корпусов (добавить еще один if) - проверить на проверенной модели
# написать тесты к коду с готовым декодером
# начать писать проверку переходов у преподов
# организовать ввод через консоль
# табличку с расписанием оформить в виде файла
# можно еще декодировать после полного составления расписания - переводом словаря расписания в датафрейм и просто
# по столбцам пройтись и по сути готово

# реализовать равномерное распределение академ. часов по неделе

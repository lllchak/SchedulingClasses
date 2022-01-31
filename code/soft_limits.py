def windows_check(timetable_data, teacher, time_slot, day_of_week, week):
	res = 0
	for group in timetable_data.keys():
		if (timetable_data[week][group][day_of_week][(time_slot % 10)+1][3] == teacher
			or timetable_data[week][group][day_of_week][(time_slot % 10)-1][3] == teacher) \
			and timetable_data[week][group][day_of_week][(time_slot % 10)][3] != teacher:
			res = 1.0

	return res


# проверка на наличие переходов между корпусами в перерыве
def corpus_check_groups(timetable_data, room, time_slot, group, day_of_week, week):
	if (timetable_data[week][group][day_of_week][(time_slot % 10) + 1][5]) % 10 == room % 10 \
			and (timetable_data[week][group][day_of_week][(time_slot % 10) - 1][5]) % 10 == room % 10:
		return 1.0

	elif (timetable_data[week][group][day_of_week][(time_slot % 10)+1][5]) % 10 == room % 10 \
			or (timetable_data[week][group][day_of_week][(time_slot % 10)-1][5]) % 10 == room % 10:
		return 0.5

	else:
		return 0.0


def less_than_5_lectures_and_seminars1(timetable_data, week, day_of_week, teacher):

	'''
    Проверяет, чтобы у преподователя было не больше 5 пар
    '''

	count = 0
	for group in timetable_data.keys():
		teacher_tuple = tuple(zip(*timetable_data[week][group][day_of_week][1:-1]))[3]
		if teacher in teacher_tuple:
			count += teacher_tuple.count(teacher)

	# Не знаю что возвращать, поэтому здесь чем больше лекций в день, тем менее привлекателен этот день
	if count > 5:
		return 0
	else:
		return (5-count) * 0.2


def less_than_3_lectures_together(timetable_dat, week, day_of_week, teacher):
	'''
	Проверяет, чтобы в расписании учителя было не больше 3-ёх лекций подряд
	'''

	teacher_schedule_for_the_day = [0, 0, 0, 0, 0, 0]  # Для отслежавания какой тип занятия проходит у препода \
	# в определённый день(лекции, семинары и т.д.)
	for group in timetable_data.keys():
		# создаётся кортеж кортежей с помощью zip, которые разделены по категориям, и из них выбираются:
		# кортеж "требований"(requirement_tuple) и кортеж "учителей"(teachers_tuple)
		requirement_tuple, teachers_tuple = tuple(zip(*timetable_data[week][group][day_of_week][1:-1]))[2: 4]
		# Если учителя нет в "кортеже учителей"(teachers_tuple), то переключаемся на другую группу(group) в цикле.
		if teacher not in teachers_tuple:
			continue
		# Следующая строчка запустится только если if не верно, т.к. если if верно, то по идее я должен буду сменить
		# счётчик group
		for i in range(len(teachers_tuple)):  # В существующем кортеже узнаём под какими индексами нужный препод
			if teacher == teachers_tuple[i]:
				teacher_schedule_for_the_day[i] = requirement_tuple[i]  # и сразу заполняем в лист расписания учителя

	# Теперь делаем проверку расписания преподователя
	max_seq = 0
	curr_seq = 0
	i = 0
	while i < len(teacher_schedule_for_the_day):
		if teacher_schedule_for_the_day[i] == 2:
			curr_seq += 1
		else:
			max_seq = max(curr_seq, max_seq)
			curr_seq = 0
		i += 1

	if max_seq >= 3:
		return 0
	elif max_seq == 2:
		return 0.6
	elif max_seq == 1:
		return 0.3
	else:
		return 1

# так как это все по сути будут мягкие ограничения думаю их можно также пока добовлять в quality_check и потом коэф подбирать
# вставить в const
TEACHER_VALUE = 1
FIZRA_VALUE = 1
LECTURE_VALUE = 1


def fizra_check(timetable_data, teacher, time_slot, day_of_week):  # проверка на то что в день стоит одна физ-ра
    res = 0
    for group in timetable_data.keys():
        for i in range(6):
            if timetable_data[group][day_of_week][(time_slot % 10) + i][2] == 4:
                res += 1

    if res == 1:
        return 1
    else:
        return 0


def count_lessons_of_teacher(timetable_data, teacher, time_slot,
                             day_of_week):  # проверка на то что у препода не больше 5 пар в день
    res = 0
    for group in timetable_data.keys():
        if timetable_data[group][day_of_week][(time_slot % 10) + 2][3] == teacher \
                and timetable_data[group][day_of_week][(time_slot % 10) + 1][3] == teacher \
                and timetable_data[group][day_of_week][(time_slot % 10) - 1][3] == teacher \
                and timetable_data[group][day_of_week][(time_slot % 10) - 2][3] == teacher \
                and timetable_data[group][day_of_week][(time_slot % 10)][3] == teacher:
            res = 1

    return res


def lecture_day_check(timetable_data, teacher, time_slot, day_of_week):  # проверка на то что мы имеем только лекции
    res = 0
    for group in timetable_data.keys():
        for i in range(6):
            if timetable_data[group][day_of_week][(time_slot % 10) + i][2] == 1:
                res += 1
            if timetable_data[group][day_of_week][(time_slot % 10) + i][2] == 2 \
                    or timetable_data[group][day_of_week][(time_slot % 10) + i][2] == 3 \
                    or timetable_data[group][day_of_week][(time_slot % 10) + i][2] == 4:
                res += 0.1
    if type(res) == int:
        return 1
    else:
        return 0


# вставить в quality_check также
teacher_mark = TEACHER_VALUE * count_lessons_of_teacher(timetable_data, room, time_slot, group, day_of_week)
fizra_mark = FIZRA_VALUE * fizra_check(timetable_data, room, time_slot, group, day_of_week)
lecture_mark = LECTURE_VALUE * lecture_day_check(timetable_data, room, time_slot, group, day_of_week)

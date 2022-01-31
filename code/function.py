# так как это все по сути будут мягкие ограничения думаю их можно также пока добовлять в quality_check и потом коэф подбирать
# вставить в const
TEACHER_VALUE = 1
FIZRA_VALUE = 1
LECTURE_VALUE = 1
LECTURE_PREPOD_VALUE = 1

def check_fizra(timetable_data, time_slot, day_of_week,group):  #  в течение учебного дня было не более одной пары по физкультуре.
    res = 0
    for group in timetable_data.keys():
        for i in range(6):
            if timetable_data[group][day_of_week][(time_slot % 10) + i][2] == 4:
                res += 1

    if res == 1:
        return 1
    else:
        return 0


def check_lessons_of_teacher(timetable_data, teacher, time_slot, day_of_week,group):  # Каждый преподаватель в течение дня должен иметь не более 5-ти пар.
    res = 0
    for group in timetable_data.keys():
        if timetable_data[group][day_of_week][(time_slot % 10) + 2][3] == teacher \
                and timetable_data[group][day_of_week][(time_slot % 10) + 1][3] == teacher \
                and timetable_data[group][day_of_week][(time_slot % 10) - 1][3] == teacher \
                and timetable_data[group][day_of_week][(time_slot % 10) - 2][3] == teacher \
                and timetable_data[group][day_of_week][(time_slot % 10)][3] == teacher:
            res = 1

    return res

def check_lecture_of_teacher(timetable_data, teacher, time_slot, day_of_week): # Каждый преподаватель в течение дня не должен иметь более 3-х лекций подряд.
    res = 0
    for group in timetable_data.keys():
        if timetable_data[group][day_of_week][(time_slot % 10) + 1][3] == teacher \
                and timetable_data[group][day_of_week][(time_slot % 10) + 1][2] == 1 \
                or timetable_data[group][day_of_week][(time_slot % 10) - 1][3] == teacher \
                and timetable_data[group][day_of_week][(time_slot % 10) - 1][2] == 1 \
                and timetable_data[group][day_of_week][(time_slot % 10)][3] == teacher:
            res = 1

    return res

def check_lecture_day(timetable_data, room, time_slot, group, day_of_week):  # проверка на то что мы имеем только лекции
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
teacher_mark = TEACHER_VALUE * check_lessons_of_teacher(timetable_data, teacher, time_slot, day_of_week,group)
fizra_mark = FIZRA_VALUE * check_fizra(timetable_data, time_slot, day_of_week,group)
lecture_mark = LECTURE_VALUE * check_lecture_day(timetable_data, room, time_slot, group, day_of_week)
lecture_prepod_value = LECTURE_PREPOD_VALUE * check_lecture_of_teacher(timetable_data, teacher, time_slot, day_of_week)
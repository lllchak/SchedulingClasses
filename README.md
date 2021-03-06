# Проект Расписание
Здесь будет храниться все, что относится к нашему проекту - описание основного
алгоритма по функциям, а также все нужные для работы файлы.

---

# Небольшое описание алгоритма

## Краткое описание общей логики

Когда данные поступают в код, они сразу же кодируются и работает основная
часть кода именно с числами (только на этапе постановки занятия в расписание
числа декодируются обратно в строки). Все работает в цикле, на каждой итерации
происходить обработка ровно одного занятия состоящего из следующих элементов:
- группа 
- название занятия
- требование к занятию
- преподаватель

Конкретное занятие это строка таблички закодированных данных, из этих строк делается
массив, по которому алгоритм и итерируется. 

После, происходит проверка жестких огриничений и отбираются те тайм-слоты,
которые им удовлетворяют. Дальше считается качество каждой из пар
тайм-слот - аудитория через проверку мягких ограничений, отбирается лучшая 
по качеству пара, декодируются значения данного занятия и занятие ставится в
расписание. 

На всех следующих итерациях выполнение жестких ограничений и качество 
определяется с условием того, что предыдущие занятия уже поставлены в 
расписание.

---

## Функции

### Проверка соблюдения ограничений 

#### checker 
Основная фукция проверки всех жестких ограничений, 
в ней из всех возможных тайм-слотов выбираются только те,
которые удовлетворяют всем жестким ограничениям

#### windows_check
Функция проверки наличия окон между занятиями у преподавателей.
Смотрит предыдущее и следующее после занятия.

#### corpus_check 
Функция проверки переходов между корпусами для групп у рядом
стоящих занятий. Также смотри предыдущее и следующее после занятия.

#### quality_check 
Основная функция подсчета качества и поиска максимального
качества. Перебирает все возможные пары тайм-слот - аудитория.

#### count_lessons 
Вспомогательная функция для подсчета количества занятий в 
дне.

### Обработка данных ('*' - используется только в test_chars)

#### encoder* 
Кодирует каждый столбец эксельной таблички числами от 1 
до количества уникальных значений в столбце

#### decoder* 
Декодирует числовые значения в исходные (возвращает 
в 'эксельный' вид)

#### data_preprocessing 
Забирает из массива конкретного занятия значения 
для дальнейшей работы (преподаватель, группа, требование по аудитории, 
все возможные тайм-слоты) 

#### dict_generator
Генерирует словарь: ключ - тайм-слот (отобран по жестким
ограничениям), значение - все возможные аудитории по этому тайм-слоту

#### dict_cleaner 
Удаляет из словаря, который сгенрировал dict_generator
значение аудитории которая была выбрана как лучшая для кокретного тайм-слота

#### lesson_filler 
Ставит занятие в расписание (обновляет timetable_data)

### Остальное

#### lesson_cycle 
Функция для итерирования по массиву занятий
(массив из строк таблички, которую вернет encoder), которые нужно
расставить (забираются из эксельной таблички)

#### output 
Просто выводит готовое расписанив в консоль

---

## Данные 

### Папка code, файл data.py (контейнеры)

#### timetable_data_nums/chars 
Вложенный словарь основного расписания (куда 
ставятся занятия и на чем считается качество): первый ключ - номер группы, 
второй ключ - номер дня недели, значение - расписание на конкретный день.

P.S. по значениям в самом вложенном списке: 
- 1 - группа 
- 2 - занятие
- 3 - требование
- 4 - преподаватель
- 5 - тайм-слот
- 6 - аудитория

#### rooms_data 
Вложенный словарь, содержащий все пары тайм-слот - аудитория: первый ключ -  
требование по аудитории (комп. класс, спорт. зал и т. д.), второй ключ -  
тайм-слот, значение - все доступные аудитории по этому тайм-слоту.

### Папка code, файл data.py (функции)

#### send_timetable_data_nums 
Возвращает словарь расписания с числовыми значениями

#### send_timetable_data_chars 
Возвращает словарь распасиния со строковыми значениями

#### send_rooms_data 
Возвращает словарь всех пар тайм-слот - аудитория

### Папка data (эксель таблички)

#### то_что_отдадут 
Табличка со значениями, типов занятий (лекция, семинар и т. д.),
преподавателей которые их ведут, групп, у которых эти занятия проходят, нагрузка,
и т. д. (в общем, тот файл, который составляет Маслякова)

#### то_что_отдадут_числа 
Из названия - тот же файл что и то_что_отдадут, просто
точная его копия с числовыми значениями вместо строк




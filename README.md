## Алгоритм агрегации статистических данных о зарплатах сотрудников

Задачи в рамках этого проекта: 
1. написание алгоритма агрегации статистических данных о зарплатах сотрудников компании по временным промежуткам 
(обработка запроса). Данные хранятся в СУБД MongoDB;
2. разработка Telegram Bot для взаимодействия с пользователем (получение запроса/ выдача результата), 
используя асинхронную библиотеку aiogram.

**Алгоритм принимает на вход**:

1. Дату и время старта агрегации. 
2. Дату и время окончания агрегации.
3. Тип агрегации. Типы агрегации могут быть следующие: час, день, месяц.

Входные данные могут быть получены от пользователя 3-мя способами:

**Получение входных данных №1 (кнопки)**:
Пользователь выбирает даты и тип агрегации, нажимая всплывающие кнопки клавиатуры 
с календарем и вариантами агрегации. 

**Пример входных данных №2(обычный текст)**:
Пользователь пишет запрос в свободном формате, например:
"Необходимо агрегировать выплаты с 1 сентября 2022 года по 31 декабря 2022 года, 
тип агрегации по месяцу."

**Пример входных данных №3**:
Пользователь вводит запрос в определенном формате, где 
"dt_from" - дата и время старта агрегации в ISO формате,
"dt_upto" - дата и время окончания агрегации в ISO формате,
"group_type" - Тип агрегации (hour, day, month).

например:
{
"dt_from":"2022-09-01T00:00:00",
"dt_upto":"2022-12-31T23:59:00",
"group_type":"month"
}

**На выходе алгоритм формирует ответ содержащий:**

1. Агрегированный массив данных (далее dataset),
2. Подписи к значениям агрегированного массива данных в ISO формате (далее labels).

**Пример ответа:**
{"dataset": [5906586, 5515874, 5889803, 6092634], "labels": ["2022-09-01T00:00:00", "2022-10-01T00:00:00", 
"2022-11-01T00:00:00", "2022-12-01T00:00:00"]}
В нулевом элементе датасета содержится сумма всех выплат за сентябрь, в первом элементе 
сумма всех выплат за октябрь и т.д. В лейблах подписи соответственно элементам датасета.

## Стэк:

- python 3.11
- Asyncio
- MongoDB 
- aiogram 3
- pytest



https://github.com/Nataly-Pro/static_agregation_bot/assets/135797064/d0a7569a-eb49-4696-a59a-a06b2736e2f1


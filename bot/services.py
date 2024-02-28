import re
from datetime import datetime as dt

from bot.MongoDB import collection

GROUP_BY = {
    "month": "%Y-%m-01T00:00:00",
    "day": "%Y-%m-%dT00:00:00",
    "hour": "%Y-%m-%dT%H:00:00",
}

months = {}
keys = ["января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"]
for i in range(1, 10):
    months[keys[i-1]] = "0" + str(i)
for i in range(10, 13):
    months[keys[i - 1]] = str(i)

#query = '{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-10-31T23:59:00", "group_type": "month"}'

#text = "Необходимо посчитать суммы всех выплат с 28.02.2022 по 31.03.2022, единица группировки - день."


async def get_report(query: dict | str) -> dict:
    """Получает запрос, берёт из него параметры (начальную и конечную даты,
    тип группировки данных), агрегирует по ним данные из БД
    и формирует отчет в определенном формате.
    """
    if not isinstance(query, dict):
        text = query
        query = {}
        array_text = text.split('"')
        keys = array_text[1:-1:4]
        values = array_text[3:-1:4]
        for i in range(3):
            query[keys[i]] = values[i]

    if not isinstance(query["dt_from"], dt):
        dt_from, dt_upto = dt.fromisoformat(query["dt_from"]), dt.fromisoformat(query["dt_upto"])
    else:
        dt_from, dt_upto = query["dt_from"], query["dt_upto"]

    pipeline = [{"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
                {"$group": {
                  "_id": {"$dateToString": {"format": GROUP_BY.get(query["group_type"]), "date": "$dt"}},
                  "total": {"$sum": "$value"}}},
                {"$sort": {"_id": 1}}
                ]

    cursor = collection.aggregate(pipeline)
    docs = await cursor.to_list(None)

    dataset = [d['total'] for d in docs]
    labels = [d['_id'] for d in docs]

    return {"dataset": dataset, "labels": labels}


async def get_data_from_text(text: str) -> dict | str:
    """Ищет в стандартном текстовом сообщении необходимые данные:
    начальную и конечную даты, тип группировки данных.
    Возвращает словарь query.
    """
    dates = []
    for key_word in ['с ', 'по ']:
        start_index = re.search(key_word, text).end()
        end_index = re.search(key_word+r'[0-9]{1,4}\W[0-9а-я]+\W[0-9]{1,4}', text).end()
        text_date = text[start_index:end_index]
        array_date = re.split(r'[/ .-]', text_date)
        if len(array_date[0]) == 1:
            array_date[0] = "0" + array_date[0]
        if len(array_date[0]) == 2:
            array_date.reverse()
        if not array_date[1].isdigit():
            array_date[1] = months.get(array_date[1])
        date = "-".join(array_date)
        dates.append(date)

    if re.search(r'час\w*', text):
        group_type = 'hour'
    elif re.search(r'день|дням|дни', text):
        group_type = 'day'
    elif re.search(r'месяц\w*', text):
        group_type = 'month'

    query = {'dt_from': dates[0] + "T00:00:00",
             'dt_upto': dates[1] + "T23:59:00",
             'group_type': group_type}

    return query


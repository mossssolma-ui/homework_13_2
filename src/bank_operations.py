import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Функция принимает список словарей с данными о банковских операциях и строку поиска.
    Возвращает список словарей, у которых в описании есть данная строка
    """
    if not search:
        return data.copy()

    pattern = re.compile(search, re.IGNORECASE)

    filtered_data = []
    for transact in data:
        description = transact.get("description")
        if not description:
            continue
        if pattern.search(str(description)):
            filtered_data.append(transact)
    return filtered_data


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Функция принимает список словарей с данными о банковских операциях и список категорий операций.
    Возвращает словарь, у которыго ключи - категории,
    а значение - количество операций в каждой категории.
    """
    if not categories:
        return {}

    descriptions = [d["description"] for d in data if d.get("description") in categories]

    counted = dict(Counter(descriptions))
    result = {category: counted.get(category, 0) for category in categories}

    return result

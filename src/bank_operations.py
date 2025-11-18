import re


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
        description = transact.get('description')
        if not description:
            continue
        if pattern.search(str(description)):
            filtered_data.append(transact)
    return filtered_data

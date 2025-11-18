import pytest
from src.bank_operations import process_bank_search, process_bank_operations


# функция process_bank_search
def test_process_bank_search_empty_search(sample_transactions):
    """Пустая строка возвращает копию исходного списка"""
    result = process_bank_search(sample_transactions, '')
    assert result == sample_transactions
    assert result is not sample_transactions


def test_process_bank_search_ignore_case(sample_transactions):
    """Поиск не чувствителен к регистру"""
    result = process_bank_search(sample_transactions, 'ОТКРЫТИЕ ВКЛАДА')
    assert len(result) == 1
    assert result[0]['id'] == '1'


def test_process_bank_search_no_description_key():
    """Транзакция без ключа 'description' не вызывает ошибку и игнорируется."""
    data = [
        {"id": "1", "amount": 100},  # нет 'description'
        {"id": "2", "description": "Открытие", "amount": 1200}
    ]
    result = process_bank_search(data, "открытие")
    assert len(result) == 1
    assert result[0]["id"] == "2"


def test_process_bank_search_description_is_none():
    """Транзакция с description = None игнорируется."""
    data = [
        {"description": None},
        {"description": "Перевод"}
    ]
    result = process_bank_search(data, "перевод")
    assert len(result) == 1
    assert result[0]["description"] == "Перевод"


def test_process_bank_search_special_regex_chars():
    """Поиск строки с регулярными выражениями."""
    data = [{"description": "Открытие вклада 120$"}]

    result = process_bank_search(data, "120$")
    assert result == []  # ожидаемо для текущей логики

    result2 = process_bank_search(data, "120")
    assert len(result2) == 1


def test_process_bank_search_empty_data():
    """Поиск по пустому списку транзакций."""
    result = process_bank_search([], "текст")
    assert result == []


# функция process_bank_operations
def test_process_bank_operations():
    """Тест на подсчет категорий"""
    data = [
        {'description': "Перевод с карты на карту"},
        {'description': "Открытие счета"},
        {'description': "Открытие счета"},
        {'description': "Открытие счета"},
        {'description': "Перевод организации"},
        {'description': "Перевод организации"},
    ]
    categories = ["Перевод с карты на карту", "Открытие счета", "Перевод организации"]
    result = process_bank_operations(data, categories)
    assert result == {'Открытие счета': 3, 'Перевод организации': 2, 'Перевод с карты на карту': 1}


def test_process_bank_operations_empty_categories():
    """Если список категорий пустой, функция возвращает пустой словарь"""
    data = [
        {'description': 'Перевод'},
        {'description': 'Открытие'},
    ]
    categories = []
    result = process_bank_operations(data, categories)
    assert result == {}


def test_process_bank_operations_empty_data():
    result = process_bank_operations([], ["A", "B"])
    assert result == {"A": 0, "B": 0}


def test_process_bank_operations_missing_category():
    data = [{"description": "Перевод"}]
    result = process_bank_operations(data, ["Перевод", "Покупка"])
    assert result == {"Перевод": 1, "Покупка": 0}

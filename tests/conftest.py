import pytest


# module masks.py
@pytest.fixture
def card_number():
    return "1596 83** **** 5199"


@pytest.fixture
def number_valid():
    return "**7890"


# module widget.py
@pytest.fixture
def card_valid():
    return "Maestro 1596 83** **** 5199"


@pytest.fixture
def account_valid():
    return "Счет **9589"


@pytest.fixture
def valid_date():
    return "11.03.2024"


# module generators.py
@pytest.fixture
def valid_transaction():
    return "Перевод организации"


# module bank_operations.py
@pytest.fixture
def sample_transactions():
    """Фикстура с примером банковских операций."""
    return [
        {"id": "1", "description": "Открытие вклада", "amount": 11500},
        {"id": "2", "description": "Перевод организации", "amount": 50000},
        {"id": "3", "description": "Перевод организации", "amount": 2000},
        {"id": "4", "description": "Перевод со счета на счет", "amount": 800},
        {"id": "5", "description": None},
        {"id": "6", "amount": 1000},
    ]

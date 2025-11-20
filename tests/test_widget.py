import pytest

from src.widget import get_date, mask_account_card


# фикстура и параметризированный тест для функции mask_account_card
def test_mask_account_card_valid(card_valid):
    assert mask_account_card("Maestro 1596837868705199") == card_valid


def test_mask_account_account_valid(account_valid):
    assert mask_account_card("Счет 64686473678894779589") == account_valid


@pytest.mark.parametrize(
    "card, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(card, expected):
    assert mask_account_card(card) == expected


@pytest.mark.parametrize(
    "input_invalid, expected",
    [
        ("", "Данные отсутствуют"),
        ("Visa", "Данные отсутствуют"),
        ("Maestro 12.34", "Данные отсутствуют"),
        ("123456789012", "Данные отсутствуют"),
    ],
)
def test_mask_account_card_invalid_inputs(input_invalid, expected):
    assert mask_account_card(input_invalid) == expected


# фикстура и параметризированный тест для функции get_date
def test_get_date(valid_date):
    assert get_date("2024-03-11T02:26:18.671407") == valid_date


@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2025-01-01T00:00:00.000000", "01.01.2025"),
        ("1999-05-07T15:30:45.123456", "07.05.1999"),
        ("2000-10-10T10:10:10.101010", "10.10.2000"),
    ],
)
def test_get_date_valid(input_date, expected):
    assert get_date(input_date) == expected


def test_get_date_range_dates():
    assert get_date("2000-01-01T00:00:00.000000") == "01.01.2000"
    assert get_date("2025-12-31T00:00:00.000000") == "31.12.2025"


@pytest.mark.parametrize(
    "invalid_dates, expected",
    [
        ("", "Некорректная дата"),
        ("2024-3-1", "Некорректная дата"),
        ("2023/12/20T12:00:00", "Некорректная дата"),
    ],
)
def test_get_date_invalid_dates(invalid_dates, expected):
    get_date(invalid_dates) == expected

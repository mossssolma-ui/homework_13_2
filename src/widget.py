from .masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card: str) -> str:
    """
    Функция обработки информации о карте и о счете.
    принимает один аргумент — строку, содержащую тип и номер карты или счета. \
    И возвращает строку с замаскированным номером.
    """
    result = "Данные отсутствуют"
    if not isinstance(account_card, str) or not account_card.strip():
        return result

    choice_acc = account_card.strip().split()
    if len(choice_acc) < 2:
        return result

    number_str = choice_acc[-1]
    try:
        number = int(number_str)
    except (ValueError, TypeError):
        return result

    if choice_acc[0] == "Счет":
        result = f"Счет {get_mask_account(number)}"
        return result

    card_name = " ".join(choice_acc[:-1])
    result = f"{card_name} {get_mask_card_number(number)}"

    return result


def get_date(date: str) -> str:
    """
    Функция возвращает дату из строки определенного формата.
    Принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024").
    """
    result = "Некорректная дата"
    if len(date) >= 10 and "-" in date and date.count("-") == 2:
        year, month, day = date.split("-")
        result = f"{day[:2]}.{month}.{year}"
    return result

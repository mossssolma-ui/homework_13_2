from src.csv_excel import get_convert_csv_to_list_dict, get_convert_excel_to_list_dict
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import load_financial_transactions
from src.widget import get_date, mask_account_card


def greeting() -> None:
    """Функция отображения приветствия"""
    print("Программа: Привет! Добро пожаловать в программу работы " "с банковскими транзакциями.")


def printing_menu(menu: list[str]) -> None:
    """Функция вывода меню из списка"""
    print("Выберите необходимый пункт меню:")
    print("\n".join(f"{i + 1}. Получить информацию о транзакциях из {f}а" for i, f in enumerate(menu)))


def select_menu_item(menu: list[str]) -> str:
    """Пользователь выбирает нужный пункт меню"""
    while True:
        user_input = input("Пользователь: ")
        if user_input.isdigit() and 1 <= int(user_input) <= len(menu):
            n = int(user_input)
            print(f"\nПрограмма: Для обработки выбран {menu[n - 1]}.")
            return menu[n - 1]
        print("Доступны команды: ", ", ".join(f"{i + 1}. {f}" for i, f in enumerate(menu)))


def printing_state_filtered(state_filt: list[str]) -> None:
    """Функция вывода статусов из списка"""
    print("Программа: Введите статус, по которому необходимо выполнить фильтрацию.")
    print(f"Доступные для фильтровки статусы: {' '.join(stat for stat in state_filt)}")


def select_state_item(state_filt: list[str]) -> str:
    """Пользователь выбирает статус для фильтра"""
    while True:
        user_input = input("Пользователь: ")
        if user_input.upper() in state_filt:
            print(f'Программа: Операции отфильтрованы по статусу "{user_input.upper()}"')
            return user_input.upper()
        else:
            print(f'Программа: Статус операции "{user_input}" недоступен.\n')
        printing_state_filtered(state_filt)
        print()


def format_transactions(trans: dict) -> str:
    """Форматирует транзакцию на вывод с использованием widget.py"""
    date_str = get_date(trans.get("date", ""))
    description = trans.get("description", "Не удалось прочитать")

    from_info = trans.get("from", "")
    to_info = trans.get("to", "")

    from_mask = mask_account_card(from_info) if from_info else ""
    to_mask = mask_account_card(to_info) if to_info else ""

    direction = f"{from_mask} -> {to_mask}" if from_mask else to_mask

    if "operationAmount" in trans:
        op_amount = trans["operationAmount"]
        amount = op_amount.get("amount", "0")
        currency_name = op_amount.get("currency", {}).get("name", "руб.")
    else:
        amount = str(trans.get("amount", "0"))
        currency_name = trans.get("currency_name", "руб.")

    result = f"{date_str} {description}\n{direction}\n" f"Сумма: {amount} {currency_name}"

    return result


def main() -> None:
    menu_list = ["JSON-файл", "CSV-файл", "XLSX-файл"]
    state_filtered = ["EXECUTED", "CANCELED", "PENDING"]

    # 1.Приветствие и выбор необходимого файла
    greeting()
    printing_menu(menu_list)
    print()
    select_file_type = select_menu_item(menu_list)
    print()

    # 2.Загрузка файла
    transactions = []
    if select_file_type == "JSON-файл":
        transactions = load_financial_transactions("data/operations.json")
    elif select_file_type == "CSV-файл":
        transactions = get_convert_csv_to_list_dict("data/transactions.csv")
    elif select_file_type == "XLSX-файл":
        transactions = get_convert_excel_to_list_dict("data/transactions_excel.xlsx")

    if not transactions:
        print("Программа: Не удалось загрузить транзакции")
        return

    # 3.Фильтрация по статусу
    printing_state_filtered(state_filtered)
    print()
    select_state = select_state_item(state_filtered)
    filtered_transactions = filter_by_state(transactions, select_state)

    # 4.Сортировка по дате
    print("Программа: Отсортировать операции по дате? Да/Нет")
    check_user_sort = input("Пользователь: ").strip().lower()
    if check_user_sort == "да":
        print("Программа: Отсортировать по возрастанию или по убыванию?")
        user_select = input("Пользователь: ").strip().lower()
        user_reverse = "убыв" in user_select
        filtered_transactions = sort_by_date(filtered_transactions, key_sort=user_reverse)

    # 5.Только рублевые транзакции
    print("Программа: Выводить только рублевые транзакции? Да/Нет")
    check_user_rub = input("Пользователь: ").strip().lower()
    if check_user_rub == "да":
        filtered_transactions = list(filter_by_currency(filtered_transactions, "руб."))

    # 6.Фильтр по слову в описании
    print("Программа: Отфильтровать список транзакций " "по определенному слову в описании? Да/Нет")
    check_user_desc = input("Пользователь: ").strip().lower()
    if check_user_desc == "да":
        print("Программа: Введите слово для поиска: ")
        search_word = input("Пользователь: ").strip().lower()
        if search_word:
            filtered_transactions = [
                trans for trans in filtered_transactions if search_word in str(trans.get("description", "")).lower()
            ]

    # 7.Вывод
    print("Программа: Распечатываю итоговый список транзакций...")

    if not filtered_transactions:
        print("Программа: Не найдено ни одной транзакции, " "подходящей под ваши условия фильтрации")
        return

    print("Программа:")
    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
    print()

    for filt in filtered_transactions:
        print(format_transactions(filt))
        print()


if __name__ == "__main__":
    main()

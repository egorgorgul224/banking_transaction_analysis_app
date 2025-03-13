from datetime import datetime
from typing import Union

from file_reader import get_excel_file


def get_greeting() -> str:
    """Функция возвращает приветствие исходя из времени дня(ночь, утро, день, вечер)"""

    current_time = datetime.now()
    if 6 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return "Добрый день"
    elif 18 <= current_time.hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_date_period(format_date: Union[str, datetime]) -> tuple[str, str]:
    """Функция принимает на вход дату и время в формате YYYY-MM-DD HH:MM:SS(по умолчанию текущая дата и время).
    Возвращает текущую дату и дату начала месяца в формате DD.MM.YYYY HH:MM:SS"""

    date_format_list = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"]

    for date_form in date_format_list:
        try:
            datetime_current_date = datetime.strptime(str(format_date), date_form)
            date_finish = datetime_current_date.strftime("%d.%m.%Y %H:%M:%S")
        except ValueError:
            continue

    date_start = (
        datetime.now()
        .replace(
            year=datetime_current_date.year,
            month=datetime_current_date.month,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        .strftime("%d.%m.%Y %H:%M:%S")
    )

    return date_start, date_finish


def get_cards_number(transactions_data: list[dict], start: str, finish: str) -> list:
    """Функция принимает на вход список с транзакциями, начало периода и конец периода. Возвращает список номеров
    всех карт за данный период в формате XXXX, где X - число от 0 до 9."""

    cards_number = []

    for transaction in transactions_data:
        if start <= str(transaction.get("Дата операции")) <= finish:
            if (
                transaction.get("Номер карты") not in cards_number
                and transaction.get("Номер карты") != "Нет номера карты"
            ):
                cards_number.append(transaction.get("Номер карты"))

    return cards_number


def get_cards_spent_cashback(
    transactions_data: list[dict], cards_number: list, start: str, finish: str
) -> tuple[list, list]:
    """Функция принимает на вход список с транзакциями, список карт, начало периода и конец периода. Возвращает список
    суммы трат и кэшбека по каждой карте."""

    total_spent = []
    cashback = []

    for card in cards_number:
        expence_count = 0
        for transaction in transactions_data:
            if (
                start <= transaction.get("Дата операции", "01.01.1980") <= finish
                and transaction.get("Номер карты", "Нет номера карты") == card
                and transaction.get("Сумма платежа", 0) < 0
            ):
                expence_count += transaction.get("Сумма платежа", 0)
        total_spent.append(round(-expence_count, 2))
        cashback_sum = expence_count * 0.01
        cashback.append(round(-cashback_sum, 2))

    return total_spent, cashback


def get_cards_info(cards_number: list, total_spent: list, cashback: list) -> list[dict]:
    """Функция принимает на вход списки номером карт в формате *XXXX, где X - число от 0 до 9, список трат по картам
    и список кэшбеков по картам. Возвращает список словарей с данными по картам(карта, сумма трат, кэшбек)"""

    cards_info = []

    for number in range(len(cards_number)):
        info = {}
        info["last_digits"] = cards_number[number][-4:]
        info["total_spent"] = total_spent[number]
        info["cashback"] = cashback[number]
        cards_info.append(info)

    return cards_info


def get_transaction_expense_for_period(user_date: Union[str, datetime] = datetime.now()) -> dict:
    """Функция принимает дату в формате YYYY-MM-DD HH:MM:SS и возвращает данные о сумме расходов и кэшбеку по каждой
    карте в периоде с начала месяца по дату пользователя(месяц берется из даты пользователя)"""

    result_info = {}
    user_greeting = get_greeting()
    transactions_data = get_excel_file()
    start, finish = get_date_period(user_date)
    cards_number = get_cards_number(transactions_data, start, finish)
    total_spent, cashback = get_cards_spent_cashback(transactions_data, cards_number, start, finish)

    result = get_cards_info(cards_number, total_spent, cashback)

    result_info["greeting"] = user_greeting
    result_info["cards"] = result

    return result_info


if __name__ == "__main__":
    print(get_transaction_expense_for_period("2020-03-04 19:44:00"))

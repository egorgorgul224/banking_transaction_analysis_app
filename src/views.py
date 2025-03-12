from datetime import datetime
from typing import Union

import pandas as pd
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


def get_transaction_expense_for_period(user_date: str = datetime.now()) -> tuple[list, list, list]:
    """Функция принимает дату в формате YYYY-MM-DD HH:MM:SS и возвращает данные о сумме расходов и кэшбеку по каждой
    карте в периоде с начала месяца по дату пользователя(месяц берется из даты пользователя)"""

    cards_number = []
    total_spent = []
    cashback = []

    transactions_data = get_excel_file()
    start, finish = get_date_period(user_date)

    for transaction in transactions_data:
        if start <= transaction.get("Дата операции") <= finish:
            if (
                transaction.get("Номер карты") not in cards_number
                and transaction.get("Номер карты") != "Нет номера карты"
            ):
                cards_number.append(transaction.get("Номер карты"))

    for card in cards_number:
        expence_count = 0
        for transaction in transactions_data:
            if (
                start <= transaction.get("Дата операции") <= finish
                and transaction.get("Номер карты") == card
                and transaction.get("Сумма платежа") < 0
            ):
                expence_count += transaction.get("Сумма платежа")
        total_spent.append(round(expence_count, 2))
        cashback_sum = expence_count * 0.01
        cashback.append(round(cashback_sum, 2))

    return cards_number, total_spent, cashback


if __name__ == "__main__":
    print(get_greeting())
    print(get_transaction_expense_for_period("2020-03-04 19:44:00"))

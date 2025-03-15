from datetime import datetime
from typing import Union

from src.file_reader import get_excel_file
from src.views import get_greeting, get_date_period, get_cards_number, get_cards_spent_cashback, get_cards_info


def main(user_date: Union[str, datetime] = datetime.now()) -> dict:
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
    print(main("2020-03-04 19:44:00"))

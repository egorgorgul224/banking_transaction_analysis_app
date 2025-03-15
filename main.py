import json
from datetime import datetime
from typing import Union

from src.external_api import get_currency_rates, get_stock_prices
from src.file_reader import get_excel_file
from src.views import (get_cards_info, get_cards_number, get_cards_spent_cashback, get_date_period, get_greeting,
                       get_period_transactions, get_top_amount_transactions)


def main(user_date: Union[str, datetime] = datetime.now()) -> str:
    """Функция принимает дату в формате YYYY-MM-DD HH:MM:SS и возвращает данные о сумме расходов и кэшбеку по каждой
    карте в периоде с начала месяца по дату пользователя(месяц берется из даты пользователя)"""

    result_info = {}
    user_greeting = get_greeting()
    transactions_data = get_excel_file()
    start, finish = get_date_period(user_date)
    transactions_info = get_period_transactions(transactions_data, start, finish)
    cards_number = get_cards_number(transactions_info)
    total_spent, cashback = get_cards_spent_cashback(transactions_info, cards_number)

    result_cards_info = get_cards_info(cards_number, total_spent, cashback)
    result_top_transactions = get_top_amount_transactions(transactions_info)
    currency_result = get_currency_rates()
    stocks_result = get_stock_prices()

    result_info["greeting"] = user_greeting
    result_info["cards"] = result_cards_info
    result_info["top_transactions"] = result_top_transactions
    result_info["currency_rates"] = currency_result
    result_info["stock_prices"] = stocks_result

    json_result = json.dumps(result_info, ensure_ascii=False)

    return json_result


if __name__ == "__main__":
    print(main("2020-03-04 19:44:00"))

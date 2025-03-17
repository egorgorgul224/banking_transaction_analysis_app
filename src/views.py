import logging
from datetime import datetime
from pathlib import Path
from typing import Union

from src.external_api import get_currency_rates, get_stock_prices
from src.file_reader import get_excel_file
from src.utils import (get_cards_info, get_cards_number, get_cards_spent_cashback, get_date_period, get_greeting,
                       get_period_transactions, get_top_amount_transactions)

BASEDIR = Path(__file__).resolve().parent.parent
logg_path = Path(BASEDIR / "logs")


logger = logging.getLogger("views")
file_handler = logging.FileHandler(f"{logg_path}/views.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_info_page_main(user_date: Union[str, datetime] = datetime.now()) -> dict:
    """Функция возвращает список, состоящий из приветствия, данных о сумме расходов и кэшбека по каждой карте в период
    с начала месяца по дату пользователя(месяц берется из даты пользователя), топ 5 транзакций по сумме платежа,
    курсу валют, стоимости акций"""

    result_info: dict = {}
    user_greeting = get_greeting()
    logger.info("Успешное выполнение функции get_greeting. Приветствие получено")
    transactions_data = get_excel_file()
    logger.info("Успешное выполнение функции get_excel_file. Получены данные по транзакциям")
    start, finish = get_date_period(user_date)
    logger.info("Успешное выполнение функции get_date_period. Получены начальная и конечная дата для фильтра")
    transactions_info = get_period_transactions(transactions_data, start, finish)
    logger.info("Успешное выполнение функции get_period_transactions. Получены данные по транзациям за период")
    cards_number = get_cards_number(transactions_info)
    logger.info("Успешное выполнение функции get_cards_number. Получены все карты за данный период")
    total_spent, cashback = get_cards_spent_cashback(transactions_info, cards_number)
    logger.info("Успешное выполнение функции get_cards_spent_cashback. Получены данные по тратам и кэшбеку по картам")

    result_cards_info = get_cards_info(cards_number, total_spent, cashback)
    logger.info("Успешное выполнение функции get_cards_info. Собрана информация о карте, тратам, кэшбеку")
    result_top_transactions = get_top_amount_transactions(transactions_info)
    logger.info("Успешное выполнение функции get_top_amount_transactions. Собрали топ 5 транзакций по сумме")
    currency_result = get_currency_rates()
    logger.info("Успешное выполнение функции get_currency_rates. Получены api данные по курсам валют")
    stocks_result = get_stock_prices()
    logger.info("Успешное выполнение функции get_stock_prices. Получены api данные по акциям")

    result_info["greeting"] = user_greeting
    result_info["cards"] = result_cards_info
    result_info["top_transactions"] = result_top_transactions
    result_info["currency_rates"] = currency_result
    result_info["stock_prices"] = stocks_result

    logger.info("Успешно собраны и переданы все данные страницы 'главная' для пользователя")
    return result_info

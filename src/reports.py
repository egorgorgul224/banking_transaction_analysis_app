import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd

from src.file_reader import get_data_from_df
from src.utils import get_period_transactions

BASEDIR = Path(__file__).resolve().parent.parent
logg_path = Path(BASEDIR / "logs")

logger = logging.getLogger("reports")
file_handler = logging.FileHandler(f"{logg_path}/reports.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """Функция принимает на вход DataFrame транзакций, категорию для поиска и дату. Возвращает json-ответ с
    транзакциями в выбранной категории за последние 3 месяца от выбранной даты(если дата текущая, то последние 3
    месяца). Функция также возвращает json-ответ в файл 'spending_by_category_report' в корне проекта."""

    logger.info("Получаем начальную и конечную дату для сортировки(разница - 3 месяца)")
    if date:
        datetime_current_date = datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S")
        date_from = datetime_current_date.strftime("%d.%m.%Y %H:%M:%S")
        date_to = (datetime.strptime(date_from, "%d.%m.%Y %H:%M:%S") + timedelta(days=90)).strftime(
            "%d.%m.%Y %H:%M:%S"
        )
    else:
        datetime_current_date = datetime.now()
        datetime_current_date = datetime.strptime(str(datetime_current_date), "%Y-%m-%d %H:%M:%S.%f")
        date_to = datetime_current_date.strftime("%d.%m.%Y %H:%M:%S")
        date_from = (datetime.strptime(date_to, "%d.%m.%Y %H:%M:%S") - timedelta(days=90)).strftime(
            "%d.%m.%Y %H:%M:%S"
        )

    logger.info("Получены 2 даты. Формируем список транзакций в период 3 месяцев от начальной даты до конечной")
    transactions_data_from_period = get_period_transactions(get_data_from_df(transactions), date_from, date_to)
    logger.info(f"Список получен. Фильтруем список по категории {category}, статусу 'OK' и карте в верном формате")
    transactions_status_ok = [
        transaction
        for transaction in transactions_data_from_period
        if transaction.get("Статус", "") == "OK"
        and transaction.get("Номер карты") != "Нет номера карты"
        and transaction.get("Категория") == category
    ]

    logger.info("Получен список по категории. Форматируем данные в json-ответ")
    if transactions_status_ok:
        json_data = json.dumps(transactions_status_ok, indent=4, ensure_ascii=False)
        return json_data
    else:
        logger.info("Данные отсутствуют или выбрана неверная категория")
        return "По выбранной категории нет транзакций"

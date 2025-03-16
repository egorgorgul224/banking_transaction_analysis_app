import calendar
import json
import logging
from datetime import datetime
from pathlib import Path

from src.file_reader import get_excel_file

BASEDIR = Path(__file__).resolve().parent.parent
logg_path = Path(BASEDIR / "logs")

logger = logging.getLogger("services")
file_handler = logging.FileHandler(f"{logg_path}/services.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_categories_cashback_service(year: str, month: str) -> str:
    """Функция принимает на вход месяц и год. Возвращает категории и кэшбек транзакций за выбранный месяц и год."""

    categories_cashback: dict = {}
    start = f"01-{month}-{year} 00:00:00"
    finish = f"{str(calendar.monthrange(int(year), int(month))[-1])}-{month}-{year} 23:59:59"

    start_date = datetime.strptime(start, "%d-%m-%Y %H:%M:%S")
    finish_date = datetime.strptime(finish, "%d-%m-%Y %H:%M:%S")
    logger.info(f"Успешно приняты и созданы даты периода для сортировки: {start_date}, {finish_date}")

    logger.info("Получаем список словарей с транзакциями из excel-файла")
    transactions_data = get_excel_file()

    logger.info("Проходим по транзакциям и создаем словарь 'категория: траты' за выбранный период")
    for transaction in transactions_data:
        current_time = datetime.strptime(str(transaction.get("Дата операции")), "%d.%m.%Y %H:%M:%S")
        if start_date <= current_time <= finish_date and transaction.get("Сумма платежа", 0) < 0:
            if transaction["Категория"] in categories_cashback:
                categories_cashback[transaction["Категория"]] += transaction["Сумма операции"]
            else:
                categories_cashback[transaction["Категория"]] = transaction["Сумма операции"]

    logger.info("Проходим по словарю и пересоздаем словарь 'категория: кэшбек' по тратам за выбранный период")
    for category, expenses in categories_cashback.items():
        categories_cashback[category] = round(expenses * -0.01, 2)

    if categories_cashback:
        logger.info("Словарь успешно преобразован в json-формат")
        return json.dumps(categories_cashback, indent=4, ensure_ascii=False)
    else:
        logger.info("Передан пустой словарь. Транзакций за месяц не найдено")
        return "В выбранном месяце отсутствуют транзакции"

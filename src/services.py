import calendar
import json
from datetime import datetime

from file_reader import get_excel_file


def get_categories_cashback_service(year: str, month: str) -> str:
    """Функция принимает на вход месяц и год. Возвращает категории и кэшбек по ним за выбранный месяц и год."""

    categories_cashback = {}
    start = f"01-{month}-{year} 00:00:00"
    finish = f"{str(calendar.monthrange(int(year), int(month))[-1])}-{month}-{year} 23:59:59"

    start_date = datetime.strptime(start, "%d-%m-%Y %H:%M:%S")
    finish_date = datetime.strptime(finish, "%d-%m-%Y %H:%M:%S")

    transactions_data = get_excel_file()

    for transaction in transactions_data:
        current_time = datetime.strptime(str(transaction.get("Дата операции")), "%d.%m.%Y %H:%M:%S")
        if start_date <= current_time <= finish_date and transaction.get("Сумма платежа", 0) < 0:
            if transaction["Категория"] in categories_cashback:
                categories_cashback[transaction["Категория"]] += transaction["Сумма операции"]
            else:
                categories_cashback[transaction["Категория"]] = transaction["Сумма операции"]

    for category, expenses in categories_cashback.items():
        categories_cashback[category] = round(expenses * -0.01, 2)

    if categories_cashback:
        return json.dumps(categories_cashback, ensure_ascii=False)
    else:
        return "В выбранном месяце отсутствуют транзакции"


if __name__ == "__main__":
    print(get_categories_cashback_service("2021", "03"))

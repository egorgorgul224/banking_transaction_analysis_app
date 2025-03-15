import logging
from datetime import datetime
from typing import Union

logger = logging.getLogger("views")
file_handler = logging.FileHandler("logs/views.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_greeting() -> str:
    """Функция возвращает приветствие исходя из времени дня(ночь, утро, день, вечер)"""

    logger.info("Получаем текущую дату и время. Возвращаем приветствие в зависимости от времени дня")
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

    logger.info(f"Преобразуем {format_date} в дату формата DD.MM.YYYY HH:MM:SS")
    for date_form in date_format_list:
        try:
            datetime_current_date = datetime.strptime(str(format_date), date_form)
            date_finish = datetime_current_date.strftime("%d.%m.%Y %H:%M:%S")
        except ValueError:
            continue

    logger.info(f"Создаем вторую дату в формате 01.MM.YYYY 00:00:00")
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

    logger.info(f"Успешно созданы две даты: {date_start}, {date_finish}")
    return date_start, date_finish


def get_cards_number(transactions_data: list[dict], start: str, finish: str) -> list:
    """Функция принимает на вход список с транзакциями, начало периода и конец периода. Возвращает список номеров
    всех карт за данный период в формате XXXX, где X - число от 0 до 9."""

    cards_number = []
    start_date = datetime.strptime(start, "%d.%m.%Y %H:%M:%S")
    finish_date = datetime.strptime(finish, "%d.%m.%Y %H:%M:%S")

    logger.info("Проходим по списку транзакций и ищем карты за переданный период времени")
    for transaction in transactions_data:
        current_time = datetime.strptime(str(transaction.get("Дата операции")), "%d.%m.%Y %H:%M:%S")
        if start_date <= current_time <= finish_date:
            if (
                transaction.get("Номер карты") not in cards_number
                and transaction.get("Номер карты") != "Нет номера карты"
            ):
                cards_number.append(transaction.get("Номер карты"))

    logger.info("Передаем список с номерами карт")
    return cards_number


def get_cards_spent_cashback(
    transactions_data: list[dict], cards_number: list, start: str, finish: str
) -> tuple[list, list]:
    """Функция принимает на вход список с транзакциями, список карт, начало периода и конец периода. Возвращает список
    суммы трат и кэшбека по каждой карте."""

    total_spent = []
    cashback = []
    start_date = datetime.strptime(start, "%d.%m.%Y %H:%M:%S")
    finish_date = datetime.strptime(finish, "%d.%m.%Y %H:%M:%S")

    logger.info("Проходим по списку карт за переданный период времени и суммируем траты и кэшбек")
    for card in cards_number:
        expence_count = 0
        for transaction in transactions_data:
            current_time = datetime.strptime(str(transaction.get("Дата операции")), "%d.%m.%Y %H:%M:%S")
            if (
                start_date <= current_time <= finish_date
                and transaction.get("Номер карты", "Нет номера карты") == card
                and transaction.get("Сумма платежа", 0) < 0
            ):
                expence_count += transaction.get("Сумма платежа", 0)
        total_spent.append(round(-expence_count, 2))
        cashback_sum = expence_count * 0.01
        cashback.append(round(-cashback_sum, 2))

    logger.info("Передаем список суммы трат и кэшбека по всем картам из переданного списка")
    return total_spent, cashback


def get_cards_info(cards_number: list, total_spent: list, cashback: list) -> list[dict]:
    """Функция принимает на вход списки номером карт в формате *XXXX, где X - число от 0 до 9, список трат по картам
    и список кэшбеков по картам. Возвращает список словарей с данными по картам(карта, сумма трат, кэшбек)"""

    cards_info = []

    logger.info("Проходим по списку карт и создаем словарь с номером карты, суммой трат, суммой кэшбека")
    for number in range(len(cards_number)):
        info = {}
        info["last_digits"] = cards_number[number][-4:]
        info["total_spent"] = total_spent[number]
        info["cashback"] = cashback[number]
        cards_info.append(info)

    logger.info("Передаем список словарей по картам, сумме трат и сумме кэшбека")
    return cards_info

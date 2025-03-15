import json
import logging
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

logger = logging.getLogger("external_api")
file_handler = logging.FileHandler("logs/external_api.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

BASEDIR = Path(__file__).resolve().parent.parent


def get_user_currencies(path_file: str = "user_settings") -> Any:
    """Функция принимает на вход название json файла с пользовательскими курсами валют и акций. Возвращает словарь с
    курсами валют и названиями акций."""

    path_object = Path(BASEDIR / path_file)

    try:
        logger.info(f"Выполняем открытие и чтение файла {path_object}.json")
        with open(f"{path_object}.json", "r", encoding="utf_8") as file:
            try:
                logger.info(f"Файл открыт. Выполняем преобразование файла {path_object}.json в объект Python")
                transactions_list = json.load(file)
                return transactions_list
            except json.JSONDecodeError:
                logger.error(f"Ошибка декодирования файла {path_object}.json")
                return {}
    except FileNotFoundError:
        logger.error(f"Файл {path_object}.json не найден")
        return {}


def get_currency_rates() -> list[dict]:
    """Функция возвращает список словарей с названием курса и ставкой в рублях"""

    user_currency_stocks = get_user_currencies()
    user_currency = user_currency_stocks.get("user_currencies")
    currency_result = []

    load_dotenv()
    apilayer_key = os.getenv("APILAYER_KEY")
    payload: dict = {}
    headers = {"apikey": f"{apilayer_key}"}

    logger.info(f"Выполняем api запрос для получения данных по курсу валют")
    if user_currency:
        for currency in user_currency:
            currency_info = {}
            url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"

            try:
                response = requests.request("GET", url, headers=headers, data=payload)
                result = response.json()

                currency_info["currency"] = currency
                currency_info["rate"] = round(result["rates"]["RUB"], 2)
                currency_result.append(currency_info)

            except requests.exceptions.ConnectionError:
                logger.error("Ошибка подключения. Проверьте интернет-соединение")
            except requests.exceptions.HTTPError:
                logger.error("HTTP ошибка. Проверьте URL-адрес.")
            except requests.exceptions.RequestException:
                logger.error("Произошла ошибка.")

        logger.info("Данные успешно получены")
        return currency_result

    else:
        logger.info("Передан пустой список курса валют")
        return []

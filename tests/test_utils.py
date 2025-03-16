from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.utils import (get_cards_info, get_cards_number, get_cards_spent_cashback, get_date_period, get_greeting,
                       get_period_transactions, get_top_amount_transactions)


@patch("src.utils.datetime")
def test_get_greeting(mock_datetime: MagicMock) -> None:
    """Тест проверяет корректный вывод приветствия в зависимости от текущего времени."""
    mock_datetime.now.return_value.hour = 10
    assert get_greeting() == "Доброе утро"
    mock_datetime.now.return_value.hour = 15
    assert get_greeting() == "Добрый день"
    mock_datetime.now.return_value.hour = 20
    assert get_greeting() == "Добрый вечер"
    mock_datetime.now.return_value.hour = 2
    assert get_greeting() == "Доброй ночи"


@pytest.mark.parametrize(
    "user_data, expected_result",
    [
        ("2025-03-15 10:50:00", ("01.03.2025 00:00:00", "15.03.2025 10:50:00")),
        ("2020-06-02 07:35:20", ("01.06.2020 00:00:00", "02.06.2020 07:35:20")),
    ],
)
def test_get_date_period(user_data: str, expected_result: tuple[str, str]) -> None:
    """Тест проверяет корректный вывод двух дат в формает 01.MM-YYYY и пользовательскую дату, когда пользователь вводит
    дату."""
    assert get_date_period(user_data) == expected_result


@pytest.mark.parametrize(
    "now_data, expected_result",
    [("2025-01-08 10:50:00.585021", ("01.01.2025 00:00:00", "08.01.2025 10:50:00"))],
)
def test_get_date_period_now(now_data: datetime, expected_result: tuple[str, str]) -> None:
    """Тест проверяет корректный вывод двух дат в формает 01.MM-YYYY и текущей даты, когда пользователь не вводит
    дату."""
    assert get_date_period(now_data) == expected_result


@pytest.mark.parametrize(
    "start_date, finish_date, expected_result",
    [
        (
            "01.01.2018 00:00:00",
            "25.01.2018 23:00:00",
            [
                {
                    "Дата операции": "03.01.2018 14:55:21",
                    "Номер карты": "*0001",
                    "Сумма операции": -21.0,
                    "Валюта операции": "RUB",
                    "Сумма платежа": -21.0,
                    "Валюта платежа": "RUB",
                    "Категория": "Супермаркеты",
                    "Описание": "Тест операция 1",
                    "Бонусы (включая кэшбэк)": 0,
                }
            ],
        )
    ],
)
def test_get_period_transactions(
    transaction_list: list[dict], start_date: str, finish_date: str, expected_result: list[dict]
) -> None:
    """Тест проверяет корректный вывод списка транзакций за переданный период времени."""

    assert get_period_transactions(transaction_list, start_date, finish_date) == expected_result


@pytest.mark.parametrize(
    "start_date, finish_date, expected_result",
    [("01.01.2025 00:00:00", "25.01.2025 23:00:00", [])],
)
def test_get_period_transactions_empty(
    transaction_list: list[dict], start_date: str, finish_date: str, expected_result: list[dict]
) -> None:
    """Тест проверяет корректный вывод пустого списка транзакций за переданный период времени."""

    assert get_period_transactions(transaction_list, start_date, finish_date) == expected_result


@pytest.mark.parametrize(
    "expected_result",
    [["*0001"]],
)
def test_get_cards_number(transaction_period_list: list[dict], expected_result: list) -> None:
    """Тест проверяет корректный вывод непустого списка номеров карт в формате *XXXX, где X - число от 0 до 9, за
    период с начала месяца по переданную дату(пользовательскую или текущую)"""
    assert get_cards_number(transaction_period_list) == expected_result


@pytest.mark.parametrize(
    "expected_result",
    [[]],
)
def test_get_cards_number_empty(transaction_period_list_empty: list[dict], expected_result: list) -> None:
    """Тест проверяет корректный вывод пустого списка, если период с начала месяца по переданную
    дату(пользовательскую или текущую) не было транзакций."""
    assert get_cards_number(transaction_period_list_empty) == expected_result


@pytest.mark.parametrize(
    "cards_number, expected_result",
    [(["*0001"], ([21.0], [0.21]))],
)
def test_get_cards_spent_cashback(
    transaction_period_list: list[dict], cards_number: list, expected_result: list
) -> None:
    """Тест проверяет корректный возврат суммы трат и кэшбека по всем картам из непустого списка за переданный период
    времени."""
    assert get_cards_spent_cashback(transaction_period_list, cards_number) == expected_result


@pytest.mark.parametrize(
    "cards_number, expected_result",
    [([], ([], []))],
)
def test_get_cards_spent_cashback_empty(
    transaction_period_list_empty: list[dict], cards_number: list, expected_result: list
) -> None:
    """Тест проверяет корректный возврат пустого списка по тратам и кэшбеку из пустого списка с картами за переданный
    период времени."""
    assert get_cards_spent_cashback(transaction_period_list_empty, cards_number) == expected_result


@pytest.mark.parametrize(
    "cards_number, total_spent, cashback, expected_result",
    [
        (
            ["*0001", "*0002"],
            [100.0, 670.0],
            [1, 6.7],
            [
                {"last_digits": "0001", "total_spent": 100.0, "cashback": 1},
                {"last_digits": "0002", "total_spent": 670.0, "cashback": 6.7},
            ],
        )
    ],
)
def test_get_cards_info(cards_number: list, total_spent: list, cashback: list, expected_result: list[dict]) -> None:
    """Тест проверяет корректный вывод списка словарей по карте, сумме тратам, сумме кэшбека."""
    assert get_cards_info(cards_number, total_spent, cashback) == expected_result


@pytest.mark.parametrize(
    "cards_number, total_spent, cashback, expected_result",
    [([], [], [], [])],
)
def test_get_cards_info_empty(
    cards_number: list, total_spent: list, cashback: list, expected_result: list[dict]
) -> None:
    """Тест проверяет корректный вывод пустого списка словарей по карте, сумме тратам, сумме кэшбека."""
    assert get_cards_info(cards_number, total_spent, cashback) == expected_result


@pytest.mark.parametrize(
    "expected_result",
    [
        [{"date": "03.01.2018", "amount": 21.0, "category": "Супермаркеты", "description": "Тест операция 1"}],
    ],
)
def test_get_top_amount_transactions(transaction_period_list: list[dict], expected_result: list[dict]) -> None:
    """Тест проверяет корректный вывод списка словарей(дата операции, сумма, категория, описание) по заданному периоду
    времени."""
    assert get_top_amount_transactions(transaction_period_list) == expected_result


@pytest.mark.parametrize(
    "expected_result",
    [[]],
)
def test_get_top_amount_transactions_empty(
    transaction_period_list_empty: list[dict], expected_result: list[dict]
) -> None:
    """Тест проверяет корректный вывод пустого списка, если по заданному периоду времени не было транзакций."""
    assert get_top_amount_transactions(transaction_period_list_empty) == expected_result

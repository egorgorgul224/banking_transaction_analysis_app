from datetime import datetime
from unittest.mock import patch

import pytest

from src.views import get_cards_number, get_cards_spent_cashback, get_date_period, get_greeting


@patch("src.views.datetime")
def test_get_greeting(mock_datetime) -> None:
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
    [("01.01.2018 00:00:00", "25.01.2018 23:00:00", ["*0001"])],
)
def test_get_cards_number(
    transaction_list: list[dict], start_date: str, finish_date: str, expected_result: list
) -> None:
    """Тест проверяет корректный вывод непустого списка номеров карт в формате *XXXX, где X - число от 0 до 9, за
    период с начала месяца по переданную дату(пользовательскую или текущую)"""
    assert get_cards_number(transaction_list, start_date, finish_date) == expected_result


@pytest.mark.parametrize(
    "start_date, finish_date, expected_result",
    [("01.12.2023 00:00:00", "25.12.2023 23:00:00", [])],
)
def test_get_cards_number_empty(
    transaction_list: list[dict], start_date: str, finish_date: str, expected_result: list
) -> None:
    """Тест проверяет корректный вывод пустого списка, если период с начала месяца по переданную
    дату(пользовательскую или текущую) не было транзакций."""
    assert get_cards_number(transaction_list, start_date, finish_date) == expected_result


@pytest.mark.parametrize(
    "cards_number, start_date, finish_date, expected_result",
    [(["*0001"], "01.01.2018 00:00:00", "25.01.2018 23:00:00", ([21.0], [0.21]))],
)
def test_get_cards_spent_cashback(
    transaction_list: list[dict], cards_number: list, start_date: str, finish_date: str, expected_result: list
) -> None:
    """Тест проверяет корректный возврат суммы трат и кэшбека по всем картам из непустого списка за переданный период
    времени."""
    assert get_cards_spent_cashback(transaction_list, cards_number, start_date, finish_date) == expected_result


@pytest.mark.parametrize(
    "cards_number, start_date, finish_date, expected_result",
    [([], "01.01.2024 00:00:00", "25.01.2024 23:00:00", ([], []))],
)
def test_get_cards_spent_cashback_empty(
    transaction_list: list[dict], cards_number: list, start_date: str, finish_date: str, expected_result: list
) -> None:
    """Тест проверяет корректный возврат пустого списка по тратам и кэшбеку из пустого списка с картами за переданный
    период времени."""
    assert get_cards_spent_cashback(transaction_list, cards_number, start_date, finish_date) == expected_result

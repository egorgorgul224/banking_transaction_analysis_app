from datetime import datetime
from unittest.mock import patch

import pytest

from src.views import get_date_period, get_greeting


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


def get_cards_number() -> None:
    """"""
    pass

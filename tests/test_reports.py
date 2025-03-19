from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from freezegun import freeze_time

from src.reports import spending_by_category


@pytest.mark.parametrize(
    "category, date",
    [
        ("Фастфуд", "2020-03-03 10:00:00"),
    ],
)
@patch("src.reports.get_period_transactions")
def test_spending_by_category(mocked_get_period_transactions: MagicMock, category: str, date: str) -> None:
    """Тест проверяет корректный вывод json-ответа транзакций по выбранный категории за 3 месяца."""
    df = pd.DataFrame(
        {
            "Дата операции": ["05.03.2020 16:44:00"],
            "Номер карты": ["*7197"],
            "Статус": ["OK"],
            "Сумма платежа": ["-160.89"],
            "Категория": ["Фастфуд"],
        }
    )

    mocked_get_period_transactions.return_value = [
        {
            "Дата операции": "05.03.2020 16:44:00",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма платежа": "-160.89",
            "Категория": "Фастфуд",
        }
    ]

    result = spending_by_category(df, category, date)
    assert result == (
        "[\n"
        "    {\n"
        '        "Дата операции": "05.03.2020 16:44:00",\n'
        '        "Номер карты": "*7197",\n'
        '        "Статус": "OK",\n'
        '        "Сумма платежа": "-160.89",\n'
        '        "Категория": "Фастфуд"\n'
        "    }\n"
        "]"
    )

    mocked_get_period_transactions.assert_called_once()


@pytest.mark.parametrize(
    "category, date",
    [
        ("Фастфуд", "2020-03-03 10:00:00"),
    ],
)
@patch("src.reports.get_period_transactions")
def test_spending_by_category_empty(mocked_get_period_transactions: MagicMock, category: str, date: str) -> None:
    """Тест проверяет корректный вывод сообщения об отсутствии транзакций по выбранной категории за 3 месяца."""
    df = pd.DataFrame(
        {
            "Дата операции": ["25.12.2025 16:44:00"],
            "Номер карты": ["*7197"],
            "Статус": ["OK"],
            "Сумма платежа": ["-160.89"],
            "Категория": ["Фастфуд"],
        }
    )

    mocked_get_period_transactions.return_value = []

    result = spending_by_category(df, category, date)
    assert result == "По выбранной категории нет транзакций за период с 03.03.2020 10:00:00 по 01.06.2020 10:00:00"

    mocked_get_period_transactions.assert_called_once()


@pytest.mark.parametrize(
    "category",
    [
        "Фастфуд",
    ],
)
@patch("src.reports.get_period_transactions")
@freeze_time("2025-03-17 23:02:07.200000")
def test_spending_by_category_cur_date(mocked_get_period_transactions: MagicMock, category: str) -> None:
    """Тест проверяет корректный вывод сообщения об отсутствии транзакций по выбранной категории с текущей датой."""
    df = pd.DataFrame(
        {
            "Дата операции": ["25.12.2020 16:44:00"],
            "Номер карты": ["*7197"],
            "Статус": ["OK"],
            "Сумма платежа": ["-160.89"],
            "Категория": ["Фастфуд"],
        }
    )

    mocked_get_period_transactions.return_value = []

    result = spending_by_category(df, category)
    assert result == "По выбранной категории нет транзакций за период с 17.12.2024 23:02:07 по 17.03.2025 23:02:07"

    mocked_get_period_transactions.assert_called_once()

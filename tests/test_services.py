from unittest.mock import MagicMock, patch

import pytest

from src.services import get_categories_cashback_service


@pytest.mark.parametrize(
    "year, month",
    [
        ("2020", "03"),
    ],
)
@patch("src.services.get_excel_file")
def test_get_categories_cashback_service(mocked_get_user_currencies: MagicMock, year: str, month: str) -> None:
    """Тест проверяет корректный вывод списка категорий и кэшбека за выбранный месяц и год."""
    mocked_get_user_currencies.return_value = [
        {
            "Дата операции": "03.03.2020 14:55:21",
            "Номер карты": "*0001",
            "Сумма операции": -21.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -21.0,
            "Валюта платежа": "RUB",
            "Категория": "Супермаркеты",
            "Описание": "Тест операция 1",
        }
    ]

    result = get_categories_cashback_service(year, month)
    assert result == '{\n    "Супермаркеты": 0.21\n}'
    mocked_get_user_currencies.assert_called_once_with()


@pytest.mark.parametrize(
    "year, month",
    [
        ("2025", "03"),
    ],
)
@patch("src.services.get_excel_file")
def test_get_categories_cashback_service_empty(mocked_get_user_currencies: MagicMock, year: str, month: str) -> None:
    """Тест проверяет корректный вывод пустого списка, если за выбранный месяц и год не было транзакций."""
    mocked_get_user_currencies.return_value = [
        {
            "Дата операции": "03.03.2020 14:55:21",
            "Номер карты": "*0001",
            "Сумма операции": -21.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -21.0,
            "Валюта платежа": "RUB",
            "Категория": "Супермаркеты",
            "Описание": "Тест операция 1",
        }
    ]

    result = get_categories_cashback_service(year, month)
    assert result == "В выбранном месяце отсутствуют транзакции"
    mocked_get_user_currencies.assert_called_once_with()

from unittest.mock import MagicMock, patch

from src.views import get_info_page_main


@patch("src.views.get_stock_prices")
@patch("src.views.get_currency_rates")
@patch("src.views.get_top_amount_transactions")
@patch("src.views.get_cards_info")
@patch("src.views.get_cards_spent_cashback")
@patch("src.views.get_cards_number")
@patch("src.views.get_period_transactions")
@patch("src.views.get_date_period")
@patch("src.views.get_data_from_df")
@patch("src.views.get_excel_df")
@patch("src.views.get_greeting")
def test_get_info_page_main(
    mock_get_greeting: MagicMock,
    mock_get_excel_df: MagicMock,
    mock_get_data_from_df: MagicMock,
    mock_get_date_period: MagicMock,
    mock_get_period_transactions: MagicMock,
    mock_get_cards_number: MagicMock,
    mock_get_cards_spent_cashback: MagicMock,
    mock_get_cards_info: MagicMock,
    mock_get_top_amount_transactions: MagicMock,
    mock_get_currency_rates: MagicMock,
    mock_get_stock_prices: MagicMock,
) -> None:
    """Тест проверяет корректный вывод итоговой информации из вызываемых функций модуля utils.py в модуле views.py."""

    mock_get_greeting.return_value = "Доброе утро"
    mock_get_excel_df.return_value = {}
    mock_get_data_from_df.return_value = [
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
    mock_get_date_period.return_value = ("01.03.2020 00:00:00", "03.03.2020 15:00:00")
    mock_get_period_transactions.return_value = [
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
    mock_get_cards_number.return_value = ["*0001"]
    mock_get_cards_spent_cashback.return_value = ([21.0], [0.21])
    mock_get_cards_info.return_value = [{"last_digits": "0001", "total_spent": 21.0, "cashback": 0.21}]
    mock_get_top_amount_transactions.return_value = [
        {"date": "03.03.2020", "amount": 21.0, "category": "Супермаркеты", "description": "Тест операция 1"}
    ]
    mock_get_currency_rates.return_value = [{"currency": "USD", "rate": 85.15}, {"currency": "EUR", "rate": 93.0}]
    mock_get_stock_prices.return_value = [
        {"stock": "AAPL", "price": 213.49},
        {"stock": "AMZN", "price": 197.95},
        {"stock": "GOOGL", "price": 165.49},
        {"stock": "MSFT", "price": 388.56},
        {"stock": "TSLA", "price": 249.98},
    ]

    result = get_info_page_main()

    expected_result = {
        "greeting": "Доброе утро",
        "cards": [{"last_digits": "0001", "total_spent": 21.0, "cashback": 0.21}],
        "top_transactions": [
            {"date": "03.03.2020", "amount": 21.0, "category": "Супермаркеты", "description": "Тест операция 1"}
        ],
        "currency_rates": [{"currency": "USD", "rate": 85.15}, {"currency": "EUR", "rate": 93.0}],
        "stock_prices": [
            {"stock": "AAPL", "price": 213.49},
            {"stock": "AMZN", "price": 197.95},
            {"stock": "GOOGL", "price": 165.49},
            {"stock": "MSFT", "price": 388.56},
            {"stock": "TSLA", "price": 249.98},
        ],
    }
    assert result == expected_result

    mock_get_greeting.assert_called_once()
    mock_get_excel_df.assert_called_once()
    mock_get_data_from_df.assert_called_once()
    mock_get_date_period.assert_called_once()
    mock_get_period_transactions.assert_called_once()
    mock_get_cards_number.assert_called_once()
    mock_get_cards_info.assert_called_once()
    mock_get_top_amount_transactions.assert_called_once()
    mock_get_currency_rates.assert_called()
    mock_get_stock_prices.assert_called()

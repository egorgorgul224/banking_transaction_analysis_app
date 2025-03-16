import json
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest
import requests

from src.external_api import get_currency_rates, get_stock_prices, get_user_currencies

BASEDIR = Path(__file__).resolve().parent.parent


def test_get_user_currencies() -> None:
    """Тест проверяет корректный вывод словаря с данным о курсе валют и акциях от пользователя из json-файла."""
    mock_data = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
    mock_json_data = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        result = get_user_currencies("fake_path")
        assert result == {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}


def test_get_user_currencies_empty_file() -> None:
    """Тест проверяет корректный вывод пустого списка, если json-файл пустой"""
    mock_data: dict = {}
    mock_json_data = json.dumps(mock_data)

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        result = get_user_currencies("fake_path")
        assert result == {}


@patch("builtins.open", new_callable=mock_open)
@patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0))
def test_get_user_currencies_json_error(mock_json_load: MagicMock, mock_open: MagicMock) -> None:
    """Тест проверяет корректную обработку ошибки JSONDecodeError"""

    result = get_user_currencies("fake_path")
    path_object = Path(BASEDIR / "fake_path")
    assert result == {}
    mock_open.assert_called_once_with(f"{path_object}.json", "r", encoding="utf_8")
    mock_json_load.assert_called_once()


@patch("builtins.open", new_callable=mock_open)
@patch("json.load", side_effect=FileNotFoundError("Expecting value", "", 0))
def test_get_user_currencies_file_not_found_error(mock_json_load: MagicMock, mock_open: MagicMock) -> None:
    """Тест проверяет корректную обработку ошибки FileNotFoundError, когда файл не найден"""

    result = get_user_currencies("fake_path")
    path_object = Path(BASEDIR / "fake_path")
    assert result == {}
    mock_open.assert_called_once_with(f"{path_object}.json", "r", encoding="utf_8")
    mock_json_load.assert_called_once()


@patch("src.external_api.get_user_currencies")
@patch("requests.request")
def test_get_currency_rates(mocked_get: MagicMock, mocked_get_user_currencies: MagicMock) -> None:
    """Тест проверяет корректный вывод списка словарей с названием курса и ставкой в рублях"""

    mocked_get_user_currencies.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = {
        "base": "USD",
        "date": "2025-03-15",
        "rates": {"RUB": 85.37},
        "success": True,
        "timestamp": 1742048104,
    }
    result = get_currency_rates()
    assert result == [{"currency": "USD", "rate": 85.37}]
    mocked_get_user_currencies.assert_called_once_with()
    mocked_get.assert_called()


@patch("src.external_api.get_user_currencies")
def test_get_currency_rates_empty(mocked_get_user_currencies: MagicMock) -> None:
    """Тест проверяет корректный пустого списка, если не были переданы курсы валют"""

    mocked_get_user_currencies.return_value = {}
    result = get_currency_rates()
    assert result == []
    mocked_get_user_currencies.assert_called_once_with()


@patch("src.external_api.get_user_currencies")
@patch("requests.request")
def test_get_currency_rates_status_code_error(
    mocked_request: MagicMock, mocked_get_user_currencies: MagicMock
) -> None:
    """Тест проверяет корректный вывод ошибки, если status code не равен 200"""

    mocked_get_user_currencies.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mocked_request.return_value.status_code = 404

    with pytest.raises(Exception) as exc_message:
        get_currency_rates()

    assert "Ошибка статус-кода: 404" in str(exc_message)
    mocked_get_user_currencies.assert_called_once_with()
    mocked_request.assert_called()


@patch("src.external_api.get_user_currencies")
@patch("requests.request")
def test_get_currency_rates_timeout_error(mocked_request: MagicMock, mocked_get_user_currencies: MagicMock) -> None:
    """Тест проверяет корректный вывод ошибки timeout"""

    mocked_get_user_currencies.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mocked_request.side_effect = requests.exceptions.Timeout

    with pytest.raises(Exception) as exc_message:
        get_currency_rates()

    assert "Время запроса истекло" in str(exc_message)
    mocked_get_user_currencies.assert_called_once_with()
    mocked_request.assert_called()


@patch("src.external_api.get_user_currencies")
@patch("requests.request")
def test_get_currency_rates_connection_error(mocked_request: MagicMock, mocked_get_user_currencies: MagicMock) -> None:
    """Тест проверяет корректный вывод ошибки connection"""

    mocked_get_user_currencies.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mocked_request.side_effect = requests.exceptions.ConnectionError

    with pytest.raises(Exception) as exc_message:
        get_currency_rates()

    assert "Ошибка подключения. Проверьте интернет-соединение" in str(exc_message)
    mocked_get_user_currencies.assert_called_once_with()
    mocked_request.assert_called()


@patch("src.external_api.get_user_currencies")
@patch("requests.request")
def test_get_currency_rates_req_exc_error(mocked_request: MagicMock, mocked_get_user_currencies: MagicMock) -> None:
    """Тест проверяет корректный вывод ошибки request exception"""

    mocked_get_user_currencies.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mocked_request.side_effect = requests.exceptions.RequestException

    with pytest.raises(Exception) as exc_message:
        get_currency_rates()

    assert "Произошла ошибка" in str(exc_message)
    mocked_get_user_currencies.assert_called_once_with()
    mocked_request.assert_called()


@patch("src.external_api.get_user_currencies")
@patch("requests.get")
def test_get_stock_prices(mocked_get: MagicMock, mocked_get_user_currencies: MagicMock) -> None:
    """Тест проверяет корректный вывод списка словарей с названием курса и ставкой в рублях"""

    mocked_get_user_currencies.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = {"c": 213.49}
    result = get_stock_prices()
    assert result == [{"stock": "AAPL", "price": 213.49}]
    mocked_get_user_currencies.assert_called_once_with()
    mocked_get.assert_called()


@patch("src.external_api.get_user_currencies")
def test_get_stock_prices_empty(mocked_get_user_currencies: MagicMock) -> None:
    """Тест проверяет корректный вывод списка словарей с названием курса и ставкой в рублях"""

    mocked_get_user_currencies.return_value = {}
    result = get_stock_prices()
    assert result == []
    mocked_get_user_currencies.assert_called_once_with()


@patch("src.external_api.get_user_currencies")
@patch("requests.get")
def test_get_stock_prices_status_code_error(mocked_request: MagicMock, mocked_get_user_currencies: MagicMock) -> None:
    """Тест проверяет корректный вывод ошибки, если status code не равен 200"""

    mocked_get_user_currencies.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mocked_request.return_value.status_code = 404

    with pytest.raises(Exception) as exc_message:
        get_stock_prices()

    assert "Ошибка статус-кода: 404" in str(exc_message)
    mocked_get_user_currencies.assert_called_once_with()
    mocked_request.assert_called()


@patch("src.external_api.get_user_currencies")
@patch("requests.get")
def test_get_stock_prices_timeout_error(mocked_request: MagicMock, mocked_get_user_currencies: MagicMock) -> None:
    """Тест проверяет корректный вывод ошибки timeout"""

    mocked_get_user_currencies.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mocked_request.side_effect = requests.exceptions.Timeout

    with pytest.raises(Exception) as exc_message:
        get_stock_prices()

    assert "Время запроса истекло" in str(exc_message)
    mocked_get_user_currencies.assert_called_once_with()
    mocked_request.assert_called()


@patch("src.external_api.get_user_currencies")
@patch("requests.get")
def test_get_stock_prices_connection_error(mocked_request: MagicMock, mocked_get_user_currencies: MagicMock) -> None:
    """Тест проверяет корректный вывод ошибки connection"""

    mocked_get_user_currencies.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mocked_request.side_effect = requests.exceptions.ConnectionError

    with pytest.raises(Exception) as exc_message:
        get_stock_prices()

    assert "Ошибка подключения. Проверьте интернет-соединение" in str(exc_message)
    mocked_get_user_currencies.assert_called_once_with()
    mocked_request.assert_called()


@patch("src.external_api.get_user_currencies")
@patch("requests.get")
def test_get_stock_prices_req_exc_error(mocked_request: MagicMock, mocked_get_user_currencies: MagicMock) -> None:
    """Тест проверяет корректный вывод ошибки request exception"""

    mocked_get_user_currencies.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mocked_request.side_effect = requests.exceptions.RequestException

    with pytest.raises(Exception) as exc_message:
        get_stock_prices()

    assert "Произошла ошибка" in str(exc_message)
    mocked_get_user_currencies.assert_called_once_with()
    mocked_request.assert_called()

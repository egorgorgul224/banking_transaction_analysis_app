from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.file_reader import get_data_from_df, get_excel_df


@patch("pandas.read_excel")
def test_get_excel_df(mock_read_excel: MagicMock) -> None:
    """Тест проверяет корректный возврат DataFrame данных с транзакциями из указанного excel файла."""

    mock_read_excel.return_value = {"id": [650703, 3598919], "state": ["EXECUTED", "EXECUTED"]}

    result = get_excel_df("fake_file")
    expected = {"id": [650703, 3598919], "state": ["EXECUTED", "EXECUTED"]}
    assert result == expected


@patch("pandas.read_excel")
def test_get_excel_df_empty(mock_read_excel: MagicMock) -> None:
    """Тест проверяет корректный возврат пустого DataFrame, если excel-файл пустой."""

    mock_read_excel.return_value = {}

    result = get_excel_df("file_empty")
    assert result == ({})


@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_get_excel_df_not_found_error(mock_read_excel: MagicMock) -> None:
    """Тест проверяет корректный возврат ошибки FileNotFoundError."""

    with pytest.raises(Exception) as exc_message:
        get_excel_df("file_not_in_project")

    assert f"Файл не найден" in str(exc_message)


@pytest.mark.parametrize(
    "expected_result",
    [
        ([{"id": 650703, "state": "EXECUTED"}, {"id": 3598919, "state": "EXECUTED"}]),
    ],
)
def test_get_excel_file(expected_result: list[dict]) -> None:
    """Тест проверяет корректный возврат списка словарей с транзакциями из указанной DataFrame таблицы."""
    result = pd.DataFrame({"id": [650703, 3598919], "state": ["EXECUTED", "EXECUTED"]})
    assert get_data_from_df(result) == expected_result


def test_get_excel_file_empty() -> None:
    """Тест проверяет корректный возврат пустого списка из пустого DataFrame."""
    result = pd.DataFrame({})
    assert get_data_from_df(result) == []

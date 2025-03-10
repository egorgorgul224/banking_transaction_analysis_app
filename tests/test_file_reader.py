from unittest.mock import patch

import pandas as pd

from src.file_reader import get_excel_file


@patch("pandas.read_excel")
def test_excel_file_reader(mock_read_excel) -> None:
    """Тест проверяет корректный возврат списка словарей с транзакциями из указанного excel файла"""

    mock_data = pd.DataFrame({"id": [650703, 3598919], "state": ["EXECUTED", "EXECUTED"]})
    mock_read_excel.return_value = mock_data

    result = get_excel_file("fake_file")
    expected = [
        {"id": 650703, "state": "EXECUTED"},
        {"id": 3598919, "state": "EXECUTED"},
    ]
    assert result == expected


@patch("pandas.read_excel")
def test_excel_file_reader_empty(mock_read_excel) -> None:
    """Тест проверяет корректный возврат пустого списка, если файл excel пустой"""

    mock_data = pd.DataFrame()
    mock_read_excel.return_value = mock_data

    result = get_excel_file("file_empty")
    assert result == []


@patch("pandas.read_excel", side_effect=FileNotFoundError)
def test_excel_file_reader_not_found_error(mock_read_excel) -> None:
    """Тест проверяет корректный возврат пустого списка, если excel файл не найден"""

    result = get_excel_file("file_not_in_project")
    assert result == []

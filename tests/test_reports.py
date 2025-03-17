from typing import Any
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.reports import spending_by_category

# @pytest.mark.parametrize(
#     "category, date",
#     [
#         ("Фастфуд", "2020-03-03 10:00:00"),
#     ],
# )
# @patch("src.reports.get_period_transactions")
# def test_spending_by_category(mocked_get_period_transactions: MagicMock, category: str, date: str) -> None:
#     """"""
#     df = pd.DataFrame(
#         {
#             "Дата операции": ["05.03.2020 16:44:00"],
#             "Номер карты": ["*7197"],
#             "Статус": ["OK"],
#             "Сумма платежа": ["-160.89"],
#             "Категория": ["Фастфуд"],
#         }
#     )
#
#     mocked_get_period_transactions.return_value = [
#         {
#             "Дата операции": "05.03.2020 16:44:00",
#             "Номер карты": "*7197",
#             "Статус": "OK",
#             "Сумма платежа": "-160.89",
#             "Категория": "Фастфуд",
#         }
#     ]
#
#     result = spending_by_category(df, category, date)
#     assert result == [
#         {
#             "Дата операции": "05.03.2020 16:44:00",
#             "Номер карты": "*7197",
#             "Статус": "OK",
#             "Сумма платежа": "-160.89",
#             "Категория": "Фастфуд",
#         }
#     ]
#
#     mocked_get_period_transactions.assert_called_once()


# @pytest.mark.parametrize(
#     "category, date",
#     [
#         ("Фастфуд", "2020-03-03 10:00:00"),
#     ],
# )
# @patch("src.reports.get_period_transactions")
# def test_spending_by_category(
#     mocked_get_period_transactions: MagicMock, category: str, date: str, capsys: Any
# ) -> None:
#     """"""
#     df = pd.DataFrame(
#         {
#             "Дата операции": ["05.03.2020 16:44:00"],
#             "Номер карты": ["*7197"],
#             "Статус": ["OK"],
#             "Сумма платежа": ["-160.89"],
#             "Категория": ["Фастфуд"],
#         }
#     )
#
#     mocked_get_period_transactions.return_value = [
#         {
#             "Дата операции": "05.03.2020 16:44:00",
#             "Номер карты": "*7197",
#             "Статус": "OK",
#             "Сумма платежа": "-160.89",
#             "Категория": "Фастфуд",
#         }
#     ]
#
#     spending_by_category(df, category, date)
#     captured = capsys.readouterr()
#     assert captured.out == ""
#
#     mocked_get_period_transactions.assert_called_once()

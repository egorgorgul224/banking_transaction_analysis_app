import json
import os
from pathlib import Path

import pandas as pd

from src.decorators import BASEDIR, write_to_json_file


def test_write_to_json_file() -> None:

    @write_to_json_file
    def my_function() -> str:
        """Тестовая функция для проверки работы декоратора."""
        df_transactions = pd.DataFrame(
            {
                "Дата операции": ["05.03.2020 16:44:00"],
                "Номер карты": ["*7197"],
                "Статус": ["OK"],
                "Сумма платежа": ["-160.89"],
                "Категория": ["Фастфуд"],
            }
        )

        operations_data = df_transactions.to_dict(orient="records")
        result = json.dumps(operations_data, ensure_ascii=False)
        return result

    my_function()

    file_path = Path(BASEDIR) / "my_function.json"

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        excepted = [
            {
                "Дата операции": "05.03.2020 16:44:00",
                "Номер карты": "*7197",
                "Статус": "OK",
                "Сумма платежа": "-160.89",
                "Категория": "Фастфуд",
            }
        ]
    assert data == excepted
    os.remove(file_path)

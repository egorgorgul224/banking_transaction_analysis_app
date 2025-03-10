import logging
from pathlib import Path

import pandas as pd

BASEDIR = Path(__file__).resolve().parent.parent

logger = logging.getLogger("file_reader")
file_handler = logging.FileHandler("logs/file_reader.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_excel_file(path_file: str = "operations.xlsx") -> list[dict]:
    """Функция принимает на вход название excel файла и возвращает список словарей с транзакциями"""

    logger.info(f"Задаем путь до файла {path_file}")
    path_object = Path(BASEDIR / "data" / path_file)
    try:
        logger.info(f"Читаем файл {path_file}")
        excel_data = pd.read_excel(path_object)
        logger.info(f"Файл {path_file} найден и прочитан успешно")
        operations_data = excel_data.to_dict(orient="records")
    except FileNotFoundError:
        logger.error(f"Файл {path_file} не найден")
        return []

    logger.info(f"Файл {path_file} успешно преобразован")
    return operations_data

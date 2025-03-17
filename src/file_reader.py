import logging
from pathlib import Path

import pandas as pd

BASEDIR = Path(__file__).resolve().parent.parent
logg_path = Path(BASEDIR / "logs")

logger = logging.getLogger("file_reader")
file_handler = logging.FileHandler(f"{logg_path}/file_reader.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_excel_df(path_file: str = "operations") -> pd.DataFrame:
    """Функция принимает на вход название excel файла и возвращает табличный формат DataFrame с транзакциями."""

    logger.info(f"Задаем путь до файла {path_file}")
    path_object = Path(f"{BASEDIR}/data/{path_file}.xlsx")
    try:
        logger.info(f"Читаем файл {path_file}")
        excel_data = pd.read_excel(path_object)
        logger.info(f"Файл {path_file} найден. Преобразуем файл в табличный формат DataFrame")
        try:
            excel_data["Номер карты"] = excel_data["Номер карты"].fillna("Нет номера карты")
        except KeyError as error:
            logger.error(f"KeyError: не найден столбец {error}")
    except FileNotFoundError:
        error_message = f"Файл не найден"
        logger.error(error_message)
        raise Exception(error_message)

    logger.info(f"Файл {path_file} успешно преобразован в табличный формат DataFrame")
    return excel_data


def get_data_from_df(df_file: pd.DataFrame) -> list[dict]:
    """Функция принимает на вход табличный формат DataFrame и возвращает список словарей транзакций."""

    if not df_file.empty:
        logger.info(f"Преобразуем DataFrame данные в список словарей")
        operations_data = df_file.to_dict(orient="records")
        logger.info(f"Успешное преобразование")
        return operations_data
    else:
        return []

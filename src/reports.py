from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from src.file_reader import get_excel_df


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """"""

    if date:
        # logger.info(f"Преобразуем {format_date} в дату формата DD.MM.YYYY HH:MM:SS")
        datetime_current_date = datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S")
        date_from = datetime_current_date.strftime("%d.%m.%Y %H:%M:%S")
        date_to = (datetime.strptime(date_from, "%d.%m.%Y %H:%M:%S") + timedelta(days=90)).strftime("%d.%m.%Y %H:%M:%S")
    else:
        datetime_current_date = datetime.now()
        datetime_current_date = datetime.strptime(str(datetime_current_date), "%Y-%m-%d %H:%M:%S.%f")
        date_to = datetime_current_date.strftime("%d.%m.%Y %H:%M:%S")
        date_from = (datetime.strptime(date_to, "%d.%m.%Y %H:%M:%S") - timedelta(days=90)).strftime("%d.%m.%Y %H:%M:%S")

    # transactions_info =



    return date_from, date_to


if __name__ == "__main__":
    print(spending_by_category(get_excel_df(), "Фастфуд",))

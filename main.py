import json
from datetime import datetime

from src.views import get_info_page_main


def main() -> str:
    """Функция возвращает приветствие, данные о сумме расходов и кэшбеку по каждой карте в периоде с начала месяца
    по дату пользователя(месяц берется из даты пользователя), топ 5 транзакций по сумме платежа, курс валют,
    стоимость акций."""

    while True:
        user_input_date = input("Введите дату в формате YYYY-MM-DD HH:MM:SS или нажмите Enter(текущая дата):")
        try:
            if user_input_date == "" or datetime.strptime(user_input_date, "%Y-%m-%d %H:%M:%S"):
                break
        except ValueError:
            print("Вы ввели некорректную дату")

    result_info = get_info_page_main(user_input_date)
    json_result = json.dumps(result_info, ensure_ascii=False)

    return json_result


if __name__ == "__main__":
    print(main())

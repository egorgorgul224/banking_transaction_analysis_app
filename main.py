import json
from datetime import datetime

from src.file_reader import get_excel_df
from src.reports import spending_by_category
from src.services import get_categories_cashback_service
from src.views import get_info_page_main


def main() -> None:
    """Функция возвращает приветствие, данные о сумме расходов и кэшбеку по каждой карте в периоде с начала месяца
    по дату пользователя(месяц берется из даты пользователя), топ 5 транзакций по сумме платежа, курс валют,
    стоимость акций. Также возвращает категории и кэшбек по ним за выбранный месяц и траты по выбранной категории
    за период 3 месяца."""

    while True:
        user_input_date = input("Введите дату в формате YYYY-MM-DD HH:MM:SS или нажмите Enter(текущая дата):")
        try:
            if user_input_date == "":
                date_object = datetime.now()
                break
            elif datetime.strptime(user_input_date, "%Y-%m-%d %H:%M:%S"):
                date_object = datetime.strptime(user_input_date, "%Y-%m-%d %H:%M:%S").date()
                break
        except ValueError:
            print("Вы ввели некорректную дату")

    user_input_category = (
        input("Введите категорию для выгрузки отчета по тратам за 3 месяца от введенной даты:").lower().capitalize()
    )

    print("Страница 'Главная': обработка информации...")
    main_info = get_info_page_main(user_input_date)
    json_main_result = json.dumps(main_info, indent=4, ensure_ascii=False)
    print(json_main_result)

    print(f"Сервис 'Выгодные категории кешбэка' за {date_object.month} месяц {date_object.year} года")
    json_service_result = get_categories_cashback_service(str(date_object.year), str(date_object.month))
    print(json_service_result)

    print("Отчет 'Траты по категории' за последние 3 месяца от/до(если не вводили дату) введенной даты")
    json_report_spending_by_category = spending_by_category(get_excel_df(), user_input_category, user_input_date)
    print(json_report_spending_by_category)


if __name__ == "__main__":
    print(main())

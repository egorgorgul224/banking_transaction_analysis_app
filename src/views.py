import datetime


def get_greeting() -> str:
    """Функция возвращает приветствие исходя из времени дня(ночь, утро, день, вечер)"""

    current_time = datetime.datetime.now()
    if 6 <= current_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_time.hour < 18:
        return "Добрый день"
    elif 18 <= current_time.hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


if __name__ == "__main__":
    print(get_greeting())

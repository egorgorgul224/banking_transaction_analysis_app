from pathlib import Path
from typing import Any, Callable, Union

BASEDIR = Path(__file__).resolve().parent.parent


def write_to_json_file(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор возвращает результат и записывает его в файл. Файл получает название функции."""

    def wrapper(*args: Any) -> Any:
        result = func(*args)

        with open(f"{Path(BASEDIR) / func.__name__}.json", "w", encoding="utf-8") as file:
            file.write(result)

        return result

    return wrapper

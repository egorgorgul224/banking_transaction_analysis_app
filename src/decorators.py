from typing import Any, Callable, Union


def write_to_json_file(func: Callable[..., Any]) -> Callable[..., Any]:
    """Декоратор получает функцию и записывает ее в файл. Файл получает название функции."""

    def wrapper(*args: Any) -> Any:
        result = func(*args)

        with open(f"{func.__name__}.json", "w", encoding="utf-8") as file:
            file.write(result)

    return wrapper

"""Цей модуль використовується для розподілу бізнес-логіки між модулями."""


def get_ordering_string(order_by: str, order_dir: str) -> str | None:
    """Ця функція повертає рядок сортування або None після перевірки переданих GET-параметрів.

    Args:
        order_by (str): Поле, за яким відбувається сортування.
        order_dir (str): Напрямок сортування.

    Returns:
        str | None: Рядок сортування або None.
    """
    if are_ordering_parameters_valid(order_by, order_dir):
        return get_order_symbol_by_(order_dir) + get_correct_(order_by)
    return None


def are_ordering_parameters_valid(order_by: str, order_dir: str) -> bool:
    """Checks if the given order_by and order_dir are valid."""
    """Ця функція перевіряє, чи валідні передані параметри order_by та order_dir.

    Args:
        order_by (str): Поле, за яким відбувається сортування.
        order_dir (str): Напрямок сортування.    

    Returns:
        bool: Чи валідні передані параметри.
    """
    if (order_dir not in ("asc", "desc")) or (order_by not in ("u", "e", "c")):
        return False
    return True


def get_order_symbol_by_(order_dir: str) -> str:
    """Ця функція повертає символ сортування Django (тире або порожній рядок).

    Args:
        order_dir (str): Напрямок сортування.

    Returns:
        str: Символ сортування.
    """
    return "-" if order_dir == "desc" else ""


def get_correct_(order_by: str) -> str:
    """Ця функція повертає правильне ім'я поля за переданим (однолітерним) order_by.

    Args:
        order_by (str): Поле, за яким відбувається сортування.

    Returns:
        str: Правильне ім'я поля.
    """
    fields = {"u": "author__username", "e": "author__email", "c": "created"}
    return fields[order_by]

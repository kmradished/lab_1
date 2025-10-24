from typing import Union, List, Tuple, Callable
from src.constants import OPERATORS


def number(token: str) -> bool:
    """
    Проверяет, является ли токен числом.
    
    :param token: Строка для проверки
    :return: True если токен можно преобразовать в число, иначе False
    """
    try:
        float(token)
        return True
    except ValueError:
        return False


def parse_number(token: str) -> int | float:
    """
    Преобразует строковый токен в числовое значение.
    
    Возвращает int если число целое, иначе float.
    
    :param token: Строковое представление числа
    :return: Числовое значение (int или float)
    """
    if "." in token:
        return float(token)
    return int(token)


def check_delete_brackets(expression: str) -> str:
    """
    Проверяет корректность расстановки скобок и удаляет их из выражения.
    
    :param expression: Математическое выражение со скобками
    :return: Выражение без скобок с нормализованными пробелами
    :raises ValueError: Если обнаружена ошибка в расстановке скобок
    """
    stack: List[int] = []
    for i, symbol in enumerate(expression):
        if symbol == "(":
            stack.append(i)
        elif symbol == ")":
            if not stack:
                raise ValueError("Ошибка со скобками (не хватает открывающей скобки)")
            stack.pop()

    if stack:
        raise ValueError("Ошибка со скобками (не хватает закрывающей скобки)")

    delete_brackets = expression.replace("(", " ").replace(")", " ")
    delete_brackets = " ".join(delete_brackets.split())

    return delete_brackets


def error_operands(operator: str, operands: list) -> None:
    """
    Проверяет корректность операндов для заданного оператора.
    
    Проверяет:
    - Для операций // и % - все операнды должны быть целыми числами
    - Для операций / и // - деление на ноль
    
    :param operator: Оператор для проверки
    :param operands: Список операндов
    :raises ValueError: Если операнды не соответствуют требованиям оператора
    :raises ZeroDivisionError: При попытке деления на ноль
    """
    if operator in ("//", "%"):
        if not all(isinstance(x, int) for x in operands):
            raise ValueError(
                f"Операция '{operands}' может использоваться только с целыми числами."
            )

    if operator in ("/", "//") and operands[-1] == 0:
        raise ZeroDivisionError("Деление на ноль")


def calculator(expression: str) -> float:
    """
    Вычисляет результат математического выражения.
    
    Поддерживает базовые арифметические операции и проверяет корректность выражения.
    
    :param expression: Математическое выражение для вычисления
    :return: Результат вычисления выражения
    :raises ValueError: Если выражение пустое, содержит ошибки или неизвестные токены
    :raises ZeroDivisionError: При делении на ноль
    """
    if not expression.split():
        raise ValueError("Пустое выражение")

    expression = check_delete_brackets(expression)
    tokens: List[str] = expression.split()
    stack: List[Union[int, float]] = []

    for i, token in enumerate(tokens):
        try:
            if number(token):
                stack.append(parse_number(token))
            elif token in OPERATORS:
                operation: Callable
                arity: int
                operation, arity = OPERATORS[token]
                if len(stack) < arity:
                    raise ValueError(f"Недостаточно операндов для операции '{token}'")
                operands: List[Union[int, float]] = []
                for _ in range(arity):
                    operands.insert(0, stack.pop())
                error_operands(token, operands)
                result: Union[int, float] = operation(*operands)
                if token in ("//", "%") and isinstance(result, float):
                    result = int(result)
                stack.append(result)
            else:
                raise ValueError(f"Неизвестный токен: '{token}'")
        except (ValueError, ZeroDivisionError):
                raise

    if len(stack) == 0:
        raise ValueError("Пустое выражение")
    elif len(stack) > 1:
        raise ValueError(f"Есть лишние значения ({stack})")
    return float(stack[0])
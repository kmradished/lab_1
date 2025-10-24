from src.constants import OPERATORS


def number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


def parse_number(token):
    if "." in token:
        return float(token)
    return int(token)


def check_delete_brackets(expression):
    stack = []
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


def error_operands(operator, operands):
    if operator in ("//", "%"):
        if not all(isinstance(x, int) for x in operands):
            raise ValueError(
                f"Операция '{operands}' может использоваться только с целыми числами."
            )

    if operator in ("/", "//") and operands[-1] == 0:
        raise ZeroDivisionError("Деление на ноль")


def calculator(expression: str):
    if not expression.split():
        raise ValueError("Пустое выражение")

    expression = check_delete_brackets(expression)
    tokens = expression.split()
    stack = []

    for i, token in enumerate(tokens):
        try:
            if number(token):
                stack.append(parse_number(token))
            elif token in OPERATORS:
                operation, arity = OPERATORS[token]
                if len(stack) < arity:
                    raise ValueError(f"Недостаточно операндов для операции '{token}'")
                operands = []
                for _ in range(arity):
                    operands.insert(0, stack.pop())
                error_operands(token, operands)
                result = operation(*operands)
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
    return stack[0]

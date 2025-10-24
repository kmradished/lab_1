from src.calculator import calculator
import pytest

def test_basic_operations():
    """Тест базовых операций"""
    assert calculator("3 4 +") == 7
    assert calculator("10 5 -") == 5
    assert calculator("3 4 *") == 12
    assert calculator("10 2 /") == 5.0
    assert calculator("7 3 //") == 2
    assert calculator("7 3 %") == 1
    assert calculator("2 3 **") == 8

def test_complex_expressions():
    """Тест сложных выражений"""
    assert calculator("3 4 2 * +") == 11  # 3 + (4 * 2)
    assert calculator("5 1 2 + 4 * + 3 -") == 14  # 5 + ((1+2)*4) - 3
    assert calculator("3 4 + 2 *") == 14  # (3 + 4) * 2

def test_unary_operations():
    """Тест унарных операций"""
    assert calculator("5 ~") == -5.0
    assert calculator("5 ~ 3 +") == -2


def test_float_numbers():
    """Тест вещественных чисел"""
    assert calculator("3.5 2.5 +") == 6.0
    assert calculator("5.5 2.5 -") == 3.0
    assert calculator("2.5 2 *") == 5.0
    assert calculator("7.5 2.5 /") == 3.0

def test_with_brackets():
    """Тест выражений со скобками (должны игнорироваться)"""
    assert calculator("(3 4 +)") == 7
    assert calculator("3 (4 2 *) +") == 11
    assert calculator("((3 4 +) 2 *)") == 14

def test_empty_expression():
    """Тест пустого выражения"""
    with pytest.raises(ValueError, match="Пустое выражение"):
        calculator("")
    with pytest.raises(ValueError, match="Пустое выражение"):
        calculator("   ")

def test_division_by_zero():
    """Тест деления на ноль"""
    with pytest.raises(ZeroDivisionError, match="Деление на ноль"):
        calculator("5 0 /")
    with pytest.raises(ZeroDivisionError, match="Деление на ноль"):
        calculator("5 0 //")

def test_integer_operations_with_floats():
    """Тест целочисленных операций с вещественными числами"""
    with pytest.raises(ValueError, match="может использоваться только с целыми числами"):
        calculator("5.5 2.5 //")
    with pytest.raises(ValueError, match="может использоваться только с целыми числами"):
        calculator("5.5 2.5 %")

def test_insufficient_operands():
    """Тест недостатка операндов"""
    with pytest.raises(ValueError, match="Недостаточно операндов"):
        calculator("5 +")
    with pytest.raises(ValueError, match="Недостаточно операндов"):
        calculator("~")

def test_unknown_token():
    """Тест неизвестного токена"""
    with pytest.raises(ValueError, match="Неизвестный токен"):
        calculator("5 4 unknown")

def test_extra_values_in_stack():
    """Тест лишних значений в стеке"""
    with pytest.raises(ValueError, match="Есть лишние значения"):
        calculator("3 4 5 +")  # 3 и результат 4+5=9 остаются в стеке

def test_unbalanced_brackets():
    """Тест несбалансированных скобок"""
    with pytest.raises(ValueError, match="не хватает закрывающей скобки"):
        calculator("(3 4 +")
    with pytest.raises(ValueError, match="не хватает открывающей скобки"):
        calculator("3 4 +)")

def test_single_number():
    """Тест одного числа"""
    assert calculator("42") == 42
    assert calculator("3.14") == 3.14

def test_multiple_spaces():
    """Тест множественных пробелов"""
    assert calculator("  3   4   +  ") == 7
    assert calculator("3    4     2     *    +") == 11

def test_negative_numbers( ):
    """Тест отрицательных чисел"""
    assert calculator("-5 3 +") == -2
    assert calculator("5 -3 +") == 2
    assert calculator("-5 -3 +") == -8

def test_exponentiation():
    """Тест возведения в степень"""
    assert calculator("2 3 **") == 8
    assert calculator("4 0.5 **") == 2.0
    assert calculator("9 0.5 **") == 3.0
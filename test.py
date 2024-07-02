import pytest

from solver_lib.solver_equation import SolverEquation
from solver_lib.solver_elements import SolverConstant
from solver_lib.solver_elements import SolverVariable


def test_single_addition():
    a = SolverConstant(3)
    b = SolverConstant(4)
    x = SolverVariable("X")

    lhs = x
    rhs = a + b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 7


def test_chained_addition():
    a = SolverConstant(3)
    b = SolverConstant(4)
    c = SolverConstant(5)
    x = SolverVariable("X")

    lhs = x
    rhs = a + b + c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 12


def test_single_subtraction():
    a = SolverConstant(8)
    b = SolverConstant(6)
    x = SolverVariable("X")

    lhs = x
    rhs = a - b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 2


def test_chained_subtraction():
    a = SolverConstant(9)
    b = SolverConstant(4)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = x
    rhs = a - b - c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 3


def test_addition_subtraction_mixed():
    a = SolverConstant(9)
    b = SolverConstant(4)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = x
    rhs = a + b - c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 11

    lhs = x
    rhs = a - b + c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 7


def test_single_multiplication():
    a = SolverConstant(3)
    b = SolverConstant(4)
    x = SolverVariable("X")

    lhs = x
    rhs = a * b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 12


def test_chained_multiplication():
    a = SolverConstant(3)
    b = SolverConstant(4)
    c = SolverConstant(5)
    x = SolverVariable("X")

    lhs = x
    rhs = a * b * c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 60


def test_addition_multiplication_mixed():
    a = SolverConstant(9)
    b = SolverConstant(4)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = x
    rhs = a * b + c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 38

    lhs = x
    rhs = a + b * c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 17


def test_single_division():
    a = SolverConstant(4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x
    rhs = a / b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and pytest.approx(result.value, abs=0.01) == 1.33


def test_chained_division():
    a = SolverConstant(12)
    b = SolverConstant(2)
    c = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x
    rhs = a / b / c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 2


def test_addition_division_mixed():
    a = SolverConstant(9)
    b = SolverConstant(4)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = x
    rhs = a / b + c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 4.25

    lhs = x
    rhs = a + b / c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 11


def test_minus_sign():
    a = SolverConstant(-4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x
    rhs = a / b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and pytest.approx(result.value, abs=0.01) == -1.33

    a = SolverConstant(4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x
    rhs = -a / b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and pytest.approx(result.value, abs=0.01) == -1.33


def test_parentheses():
    a = SolverConstant(-4)
    b = SolverConstant(3)
    c = SolverConstant(5)
    x = SolverVariable("X")

    lhs = x
    rhs = a + b * c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 11

    lhs = x
    rhs = (a + b) * c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == -5


def test_single_exponentiation():
    a = SolverConstant(4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x
    rhs = a**b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 64


def test_chained_exponentiation():
    a = SolverConstant(4)
    b = SolverConstant(3)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = x
    rhs = a**b**c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 262144

    lhs = x
    rhs = (a**b)**c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 4096


def test_switch_addition():
    a = SolverConstant(4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x + a
    rhs = b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == -1


def test_switch_subtraction():
    a = SolverConstant(4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x - a
    rhs = b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 7


def test_switch_multiplication():
    a = SolverConstant(4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x * a
    rhs = b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 0.75


def test_switch_division():
    a = SolverConstant(4)
    b = SolverConstant(3)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = x / a
    rhs = b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 12


def test_switch_addition_chained_left():
    a = SolverConstant(4)
    b = SolverConstant(3)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = a + b + x
    rhs = c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == -5


def test_switch_subtraction_chained_left():
    a = SolverConstant(4)
    b = SolverConstant(3)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = a - b + x
    rhs = c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 1


def test_switch_multiplication_chained_left():
    a = SolverConstant(4)
    b = SolverConstant(3)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = a * b * x
    rhs = c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 1 / 6


def test_switch_division_chained_left():
    a = SolverConstant(4)
    b = SolverConstant(3)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = a / b * x
    rhs = c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 2 * 3 / 4

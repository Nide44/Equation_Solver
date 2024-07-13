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

    assert result.name == x.name and sorted(result.value) == [3 + 4]


def test_chained_addition():
    a = SolverConstant(3)
    b = SolverConstant(4)
    c = SolverConstant(5)
    x = SolverVariable("X")

    lhs = x
    rhs = a + b + c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [3 + 4 + 5]


def test_single_subtraction():
    a = SolverConstant(8)
    b = SolverConstant(6)
    x = SolverVariable("X")

    lhs = x
    rhs = a - b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [8 - 6]


def test_chained_subtraction():
    a = SolverConstant(9)
    b = SolverConstant(4)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = x
    rhs = a - b - c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [9 - 4 - 2]


def test_addition_subtraction_mixed():
    a = SolverConstant(9)
    b = SolverConstant(4)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = x
    rhs = a + b - c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [9 + 4 - 2]

    lhs = x
    rhs = a - b + c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [9 - 4 + 2]


def test_single_multiplication():
    a = SolverConstant(3)
    b = SolverConstant(4)
    x = SolverVariable("X")

    lhs = x
    rhs = a * b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [3 * 4]


def test_chained_multiplication():
    a = SolverConstant(3)
    b = SolverConstant(4)
    c = SolverConstant(5)
    x = SolverVariable("X")

    lhs = x
    rhs = a * b * c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [3 * 4 * 5]


def test_addition_multiplication_mixed():
    a = SolverConstant(9)
    b = SolverConstant(4)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = x
    rhs = a * b + c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [9 * 4 + 2]

    lhs = x
    rhs = a + b * c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [9 + 4 * 2]


def test_single_division():
    a = SolverConstant(4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x
    rhs = a / b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [4 / 3]


def test_chained_division():
    a = SolverConstant(12)
    b = SolverConstant(2)
    c = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x
    rhs = a / b / c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [12 / 2 / 3]


def test_addition_division_mixed():
    a = SolverConstant(9)
    b = SolverConstant(4)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = x
    rhs = a / b + c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [9 / 4 + 2]

    lhs = x
    rhs = a + b / c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [9 + 4 / 2]


def test_minus_sign():
    a = SolverConstant(-4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x
    rhs = a / b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [-4 / 3]

    a = SolverConstant(4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x
    rhs = -a / b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [-4 / 3]


def test_parentheses():
    a = SolverConstant(-4)
    b = SolverConstant(3)
    c = SolverConstant(5)
    x = SolverVariable("X")

    lhs = x
    rhs = a + b * c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [-4 + 3 * 5]

    lhs = x
    rhs = (a + b) * c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [(-4 + 3) * 5]


def test_single_exponentiation():
    a = SolverConstant(4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x
    rhs = a**b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [4**3]


def test_chained_exponentiation():
    a = SolverConstant(4)
    b = SolverConstant(3)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = x
    rhs = a**b**c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [4**3**2]

    lhs = x
    rhs = (a**b) ** c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [(4**3) ** 2]


def test_switch_addition():
    a = SolverConstant(4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x + a
    rhs = b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [3 - 4]


def test_switch_subtraction():
    a = SolverConstant(4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x - a
    rhs = b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [4 + 3]


def test_switch_multiplication():
    a = SolverConstant(4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x * a
    rhs = b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [3 / 4]


def test_switch_division():
    a = SolverConstant(4)
    b = SolverConstant(3)
    x = SolverVariable("X")

    lhs = x / a
    rhs = b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [4 * 3]


def test_switch_addition_chained():
    a = SolverConstant(4)
    b = SolverConstant(3)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = a + b + x
    rhs = c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [2 - 4 - 3]

    lhs = x + a + b
    rhs = c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [2 - 4 - 3]


def test_switch_subtraction_chained():
    a = SolverConstant(4)
    b = SolverConstant(3)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = -a - b + x
    rhs = c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [2 + 4 + 3]

    lhs = x - a - b
    rhs = c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [2 + 4 + 3]


def test_switch_multiplication_chained():
    a = SolverConstant(4)
    b = SolverConstant(3)
    c = SolverConstant(2)
    x = SolverVariable("X")

    lhs = a * b * x
    rhs = c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [1 / 6]

    lhs = x * a * b
    rhs = c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [1 / 6]


def test_switch_division_chained():
    a = SolverConstant(1)
    b = SolverConstant(4)
    c = SolverConstant(3)
    d = SolverConstant(2)
    x = SolverVariable("X")

    lhs = a / b / c * x
    rhs = d

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [2 * 3 * 4]

    lhs = x / b / c
    rhs = d

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and sorted(result.value) == [2 * 3 * 4]

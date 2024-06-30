from solver_lib.solver_equation import SolverEquation
from solver_lib.solver_int import SolverInt
from solver_lib.solver_variable import SolverVariable


def test_single_addition():
    a = SolverInt(3)
    b = SolverInt(4)
    x = SolverVariable("X")

    lhs = x
    rhs = a + b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 7


def test_chained_addition():
    a = SolverInt(3)
    b = SolverInt(4)
    c = SolverInt(5)
    x = SolverVariable("X")

    lhs = x
    rhs = a + b + c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 12


def test_single_subtraction():
    a = SolverInt(8)
    b = SolverInt(6)
    x = SolverVariable("X")

    lhs = x
    rhs = a - b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 2


def test_chained_subtraction():
    a = SolverInt(9)
    b = SolverInt(4)
    c = SolverInt(2)
    x = SolverVariable("X")

    lhs = x
    rhs = a - b - c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 3


def test_addition_subtraction_mixed():
    a = SolverInt(9)
    b = SolverInt(4)
    c = SolverInt(2)
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
    a = SolverInt(3)
    b = SolverInt(4)
    x = SolverVariable("X")

    lhs = x
    rhs = a * b

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 12


def test_chained_multiplication():
    a = SolverInt(3)
    b = SolverInt(4)
    c = SolverInt(5)
    x = SolverVariable("X")

    lhs = x
    rhs = a * b * c

    eq = SolverEquation(lhs, rhs)
    result = eq.solve(x)

    assert result.name == x.name and result.value == 60


def test_addition_multiplication_mixed():
    a = SolverInt(9)
    b = SolverInt(4)
    c = SolverInt(2)
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
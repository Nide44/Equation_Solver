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

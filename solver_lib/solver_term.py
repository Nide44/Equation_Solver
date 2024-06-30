from solver_lib.solver_expression import SolverExpression


class SolverTerm(SolverExpression):
    def __init__(self, value=None, name=None):
        super().__init__(value=value, name=name)

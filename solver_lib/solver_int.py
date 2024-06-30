from solver_lib.solver_term import SolverTerm


class SolverInt(SolverTerm):
    def __init__(self, value):
        super().__init__(value=value)

    def __str__(self):
        return str(self.value)

    def reduce(self, _):
        return True, False, False, self.value, self

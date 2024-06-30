from solver_lib.solver_term import SolverTerm


class SolverVariable(SolverTerm):
    def __init__(self, name):
        super().__init__(name=name)

    def __str__(self):
        return str(self.name)

    def reduce(self):
        return True, True, self.name

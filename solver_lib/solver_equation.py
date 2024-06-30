from solver_lib.solver_variable import SolverVariable


class SolverEquation:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str(self.lhs) + " = " + str(self.rhs)

    def solve(self, variable):
        # self.rhs.expand()
        # self.rhs.move_var(variable)
        # self.lhs.expand()
        # self.lhs.move_values()
        rhs_solved, rhs_has_var, rhs_value = self.rhs.reduce()
        lhs_solved, lhs_has_var, _ = self.lhs.reduce()

        if rhs_solved and lhs_solved and not rhs_has_var and lhs_has_var:
            new_variable = SolverVariable(variable.name)
            new_variable.value = rhs_value
            return new_variable

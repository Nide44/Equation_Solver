class SolverExpression:
    def __init__(self, value=None, name=None, sub_expressions=None, operand=None):
        self.value = value
        self.name = name
        self.sub_expressions = sub_expressions
        self.operand = operand

    def __add__(self, other):
        return SolverExpression(sub_expressions=[self, other], operand="add")

    def __sub__(self, other):
        return SolverExpression(sub_expressions=[self, other], operand="sub")

    def __str__(self):
        if self.operand == "add":
            return " + ".join(
                [str(subexpression) for subexpression in self.sub_expressions]
            )

        elif self.operand == "sub":
            return " - ".join(
                [str(subexpression) for subexpression in self.sub_expressions]
            )

    def reduce(self):
        sub_exp_solved_list = []
        sub_exp_var_list = []
        sub_exp_value_list = []

        for sub_expression in self.sub_expressions:
            sub_exp_solved, sub_exp_var, sub_exp_value = sub_expression.reduce()
            sub_exp_solved_list.append(sub_exp_solved)
            sub_exp_var_list.append(sub_exp_var)
            sub_exp_value_list.append(sub_exp_value)

        if all(sub_exp_solved_list):
            if not any(sub_exp_var_list):
                if self.operand == "add":
                    return True, False, sub_exp_value_list[0] + sub_exp_value_list[1]
                elif self.operand == "sub":
                    return True, False, sub_exp_value_list[0] - sub_exp_value_list[1]
            else:
                pass

        else:
            pass

from solver_lib.globals import operator_sign_mapping

from solver_lib.logger import info_logger
from solver_lib.utils import Utils


class SolverExpression:
    def __init__(
        self,
        value=None,
        name=None,
        sub_expressions=[],
        operator=None,
        level=0,
    ):
        self.value = value
        self.name = name
        self.sub_expressions = sub_expressions
        self.operator = operator
        self.level = level

    def __add__(self, other):
        return self.create_new_expression(other, "add")

    def __sub__(self, other):
        return self.create_new_expression(other, "sub")

    def __mul__(self, other):
        return self.create_new_expression(other, "mul")

    def __truediv__(self, other):
        return self.create_new_expression(other, "div")

    def __neg__(self):
        new_exp = SolverConstant(-1 * self.value, level=self.level)
        return new_exp

    def __pow__(self, other):
        if other.value and (not isinstance(other.value, int) or other.value < 0):
            raise Exception("Only natural exponents are allowed in exponentiation")

        return self.create_new_expression(other, "pow")

    def __str__(self):
        return self.stringify_single_expression()

    def create_new_expression(self, other, operator):
        old_level = self.level
        new_exp = SolverExpression(
            sub_expressions=[self, other], operator=operator, level=old_level
        )
        new_exp.increase_sublevels(False)
        return new_exp

    def stringify_single_expression(self):
        return (" " + operator_sign_mapping[self.operator] + " ").join(
            [str(sub_expression) for sub_expression in self.sub_expressions]
        )

    def increase_sublevels(self, update_self):
        for sub_expression in self.sub_expressions:
            sub_expression.increase_sublevels(True)
        if update_self:
            self.level += 1

    def decrease_sublevels(self, update_self):
        for sub_expression in self.sub_expressions:
            sub_expression.decrease_sublevels(True)
        if update_self:
            self.level -= 1

    def reduce(self, top_parent):
        sub_exp_solved_list = []
        sub_exp_var_list = []

        for sub_exp_index, sub_expression in enumerate(self.sub_expressions):
            sub_exp_solved, sub_exp_updated, sub_exp_var, new_sub_exp, print_update = (
                sub_expression.reduce(top_parent)
            )
            sub_exp_solved_list.append(sub_exp_solved)
            sub_exp_var_list.append(sub_exp_var)
            if sub_exp_updated:
                self.sub_expressions[sub_exp_index] = new_sub_exp

            if print_update:
                info_logger.info("Updated equation: " + str(top_parent))

            if sub_exp_updated or isinstance(sub_expression, SolverConstant):
                sub_expression.level = 0

        if all(sub_exp_solved_list):
            if not any(sub_exp_var_list):
                value1 = self.sub_expressions[0].value
                value2 = self.sub_expressions[1].value

                if self.operator == "add":
                    add_value = value1 + value2
                    info_logger.info(f"Added {value1} and {value2} to get {add_value}")
                    return (
                        True,
                        True,
                        False,
                        SolverConstant(add_value, level=self.level),
                        True,
                    )

                elif self.operator == "sub":
                    sub_value = value1 - value2
                    info_logger.info(
                        f"Subtracted {value2} from {value1} to get {sub_value}"
                    )
                    return (
                        True,
                        True,
                        False,
                        SolverConstant(sub_value, level=self.level),
                        True,
                    )

                elif self.operator == "mul":
                    mul_value = value1 * value2
                    info_logger.info(
                        f"Multiplied {value1} with {value2} to get {mul_value}"
                    )
                    return (
                        True,
                        True,
                        False,
                        SolverConstant(
                            mul_value,
                            level=self.level,
                        ),
                        True,
                    )

                elif self.operator == "div":
                    div_value = value1 / value2
                    return (
                        True,
                        True,
                        False,
                        SolverConstant(div_value, level=self.level),
                        True,
                    )

                elif self.operator == "pow":
                    pow_value = value1**value2
                    info_logger.info(
                        f"Took {value1} to the power of {value2} to get {pow_value}"
                    )
                    return (
                        True,
                        True,
                        False,
                        SolverConstant(pow_value, level=self.level),
                        True,
                    )

        return False, False, True, self, False


class SolverTerm(SolverExpression):
    def __init__(self, value=None, name=None, level=0):
        super().__init__(value=value, name=name, level=level)


class SolverConstant(SolverTerm):
    def __init__(self, value, level=0):
        super().__init__(value=value, level=level)

    def __str__(self):
        return str(self.value)

    def reduce(self, _):
        return True, False, False, self, False


class SolverVariable(SolverTerm):
    def __init__(self, name, level=0, fraction_parentheses=False):
        super().__init__(name=name, level=level)

    def __str__(self):
        return str(self.name)

    def reduce(self, _):
        return True, False, True, self, False

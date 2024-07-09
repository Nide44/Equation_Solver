from solver_lib.globals import operator_sign_mapping

from solver_lib.logger import info_logger
from solver_lib.settings import SHOW_DECIMALS
from solver_lib.utils import Utils


class SolverExpression:
    def __init__(
        self,
        value=None,
        name=None,
        sub_expressions=[],
        operator=None,
        level=0,
        numerator=None,
        denominator=None,
    ):
        self.value = value
        self.numerator = numerator
        self.denominator = denominator
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
                numerator1 = self.sub_expressions[0].numerator
                numerator2 = self.sub_expressions[1].numerator
                denominator1 = self.sub_expressions[0].denominator
                denominator2 = self.sub_expressions[1].denominator

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

                    new_numerator = numerator1 * numerator2
                    new_denominator = denominator1 * denominator2
                    gcd = Utils.calculate_gcd(new_numerator, new_denominator)
                    new_numerator = int(new_numerator / gcd)
                    new_denominator = int(new_denominator / gcd)

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
                            numerator=new_numerator,
                            denominator=new_denominator,
                        ),
                        True,
                    )

                elif self.operator == "div":
                    div_value = value1 / value2

                    new_numerator = numerator1 * denominator2
                    new_denominator = numerator2 * denominator1
                    gcd = Utils.calculate_gcd(new_numerator, new_denominator)
                    new_numerator = int(new_numerator / gcd)
                    new_denominator = int(new_denominator / gcd)
                    if new_denominator == 1:
                        info_logger.info(
                            f"Divided {value1} by {value2} to get {div_value}"
                        )
                        print_update = True
                    else:
                        print_update = False
                    return (
                        True,
                        True,
                        False,
                        SolverConstant(
                            div_value,
                            level=self.level,
                            numerator=new_numerator,
                            denominator=new_denominator,
                        ),
                        print_update,
                    )

                elif self.operator == "pow":
                    pow_value = value1**value2

                    new_numerator = numerator1**value2
                    new_denominator = denominator1**value2
                    gcd = Utils.calculate_gcd(new_numerator, new_denominator)
                    new_numerator = int(new_numerator / gcd)
                    new_denominator = int(new_denominator / gcd)

                    info_logger.info(
                        f"Took {value1} to the power of {value2} to get {pow_value}"
                    )
                    return (
                        True,
                        True,
                        False,
                        SolverConstant(
                            pow_value,
                            level=self.level,
                            numerator=new_numerator,
                            denominator=new_denominator,
                        ),
                        True,
                    )

        return False, False, True, self, False


class SolverTerm(SolverExpression):
    def __init__(self, value=None, name=None, level=0, numerator=None, denominator=1):
        super().__init__(
            value=value,
            name=name,
            level=level,
            numerator=numerator,
            denominator=denominator,
        )


class SolverConstant(SolverTerm):
    def __init__(self, value, level=0, numerator=None, denominator=None):
        numerator = value if numerator == None else numerator
        denominator = 1 if denominator == None else denominator
        super().__init__(
            value=value, level=level, numerator=numerator, denominator=denominator
        )

    def __str__(self):
        if SHOW_DECIMALS or self.denominator == 1:
            return str(self.value)
        else:
            if self.level != 0 and self.denominator != 1:
                return "(" + str(self.numerator) + " / " + str(self.denominator) + ")"
            else:
                return str(self.numerator) + " / " + str(self.denominator)

    def reduce(self, _):
        return True, False, False, self, False


class SolverVariable(SolverTerm):
    def __init__(self, name, level=0, fraction_parentheses=False):
        super().__init__(name=name, level=level)

    def __str__(self):
        return str(self.name)

    def reduce(self, _):
        return True, False, True, self, False

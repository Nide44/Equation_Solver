from solver_lib.logger import info_logger


class SolverExpression:
    def __init__(
        self, value=None, name=None, sub_expressions=[], operand=None, level=0
    ):
        self.value = value
        self.name = name
        self.sub_expressions = sub_expressions
        self.operand = operand
        self.level = level

    def __add__(self, other):
        old_level = self.level
        new_exp = SolverExpression(
            sub_expressions=[self, other], operand="add", level=old_level
        )
        new_exp.increase_sublevels(False)
        return new_exp

    def __sub__(self, other):
        old_level = self.level
        new_exp = SolverExpression(
            sub_expressions=[self, other], operand="sub", level=old_level
        )
        new_exp.increase_sublevels(False)
        return new_exp

    def __mul__(self, other):
        old_level = self.level
        new_exp = SolverExpression(
            sub_expressions=[self, other], operand="mul", level=old_level
        )
        new_exp.increase_sublevels(False)
        return new_exp

    def __truediv__(self, other):
        old_level = self.level
        new_exp = SolverExpression(
            sub_expressions=[self, other], operand="div", level=old_level
        )
        new_exp.increase_sublevels(False)
        return new_exp

    def __neg__(self):
        new_exp = SolverConstant(-1 * self.value, level=self.level)
        return new_exp

    def __pow__(self, other):
        if other.value and (not isinstance(other.value, int) or other.value < 0):
            raise Exception("Only natural exponents are allowed in exponentiation")
        old_level = self.level
        new_exp = SolverExpression(
            sub_expressions=[self, other], operand="pow", level=old_level
        )
        new_exp.increase_sublevels(False)
        return new_exp

    def __str__(self):
        if self.operand == "add":
            if self.level > 0:
                return (
                    "("
                    + " + ".join(
                        [str(sub_expression) for sub_expression in self.sub_expressions]
                    )
                    + ")"
                )
            else:
                return " + ".join(
                    [str(sub_expression) for sub_expression in self.sub_expressions]
                )

        elif self.operand == "sub":
            if self.level > 0:
                return (
                    "("
                    + " - ".join(
                        [str(sub_expression) for sub_expression in self.sub_expressions]
                    )
                    + ")"
                )
            else:
                return " - ".join(
                    [str(sub_expression) for sub_expression in self.sub_expressions]
                )

        elif self.operand == "mul":
            if self.level > 0:
                return (
                    "("
                    + " * ".join(
                        [str(sub_expression) for sub_expression in self.sub_expressions]
                    )
                    + ")"
                )
            else:
                return " * ".join(
                    [str(sub_expression) for sub_expression in self.sub_expressions]
                )

        elif self.operand == "div":
            if self.level > 0:
                return (
                    "("
                    + " / ".join(
                        [str(sub_expression) for sub_expression in self.sub_expressions]
                    )
                    + ")"
                )
            else:
                return " / ".join(
                    [str(sub_expression) for sub_expression in self.sub_expressions]
                )

        elif self.operand == "pow":
            if self.level > 0:
                return (
                    "("
                    + " ^ ".join(
                        [str(sub_expression) for sub_expression in self.sub_expressions]
                    )
                    + ")"
                )
            else:
                return " ^ ".join(
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
        sub_exp_value_list = []

        for sub_exp_index, sub_expression in enumerate(self.sub_expressions):
            sub_exp_solved, sub_exp_updated, sub_exp_var, sub_exp_value, new_sub_exp = (
                sub_expression.reduce(top_parent)
            )
            sub_exp_solved_list.append(sub_exp_solved)
            sub_exp_var_list.append(sub_exp_var)
            sub_exp_value_list.append(sub_exp_value)
            if sub_exp_updated:
                self.sub_expressions[sub_exp_index] = new_sub_exp
                info_logger.info("Updated equation: " + str(top_parent))
            if sub_exp_updated or isinstance(sub_expression, SolverConstant):
                sub_expression.level = 0

        if all(sub_exp_solved_list):
            if not any(sub_exp_var_list):
                value1 = sub_exp_value_list[0]
                value2 = sub_exp_value_list[1]
                if self.operand == "add":
                    add_value = value1 + value2
                    info_logger.info(f"Added {value1} and {value2} to get {add_value}")
                    return (
                        True,
                        True,
                        False,
                        add_value,
                        SolverConstant(add_value, level=self.level),
                    )

                elif self.operand == "sub":
                    sub_value = value1 - value2
                    info_logger.info(
                        f"Subtracted {value2} from {value1} to get {sub_value}"
                    )
                    return (
                        True,
                        True,
                        False,
                        sub_value,
                        SolverConstant(sub_value, level=self.level),
                    )

                elif self.operand == "mul":
                    mul_value = value1 * value2
                    info_logger.info(
                        f"Multiplied {value1} with {value2} to get {mul_value}"
                    )
                    return (
                        True,
                        True,
                        False,
                        mul_value,
                        SolverConstant(mul_value, level=self.level),
                    )

                elif self.operand == "div":
                    div_value = value1 / value2
                    info_logger.info(f"Divided {value1} by {value2} to get {div_value}")
                    return (
                        True,
                        True,
                        False,
                        div_value,
                        SolverConstant(div_value, level=self.level),
                    )

                elif self.operand == "pow":
                    pow_value = value1**value2
                    info_logger.info(
                        f"Took {value1} to the power of {value2} to get {pow_value}"
                    )
                    return (
                        True,
                        True,
                        False,
                        pow_value,
                        SolverConstant(pow_value, level=self.level),
                    )

        return False, False, True, None, self


class SolverTerm(SolverExpression):
    def __init__(self, value=None, name=None, level=0):
        super().__init__(value=value, name=name, level=level)


class SolverConstant(SolverTerm):
    def __init__(self, value, level=0):
        super().__init__(value=value, level=level)

    def __str__(self):
        return str(self.value)

    def reduce(self, _):
        return True, False, False, self.value, self


class SolverVariable(SolverTerm):
    def __init__(self, name, level=0):
        super().__init__(name=name, level=level)

    def __str__(self):
        return str(self.name)

    def reduce(self, _):
        return True, False, True, self.name, self

import sys, os

from solver_lib.logger import error_logger, info_logger
from solver_lib.solver_elements import SolverConstant, SolverExpression, SolverVariable


class SolverEquation:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str(self.lhs) + " = " + str(self.rhs)

    def switch_left_to_right(self):
        for sub_exp_index, sub_expression in enumerate(self.lhs.sub_expressions):
            if isinstance(sub_expression, SolverConstant):
                original_operand = self.lhs.operand
                include_original_operand = True if sub_exp_index == 1 else False
                # LHS
                remaining_sub_exp = self.lhs.sub_expressions[1 - sub_exp_index]
                remaining_sub_exp.decrease_sublevels(True)
                self.lhs = remaining_sub_exp

                # RHS
                self.rhs.increase_sublevels(True)
                if original_operand == "add":
                    self.rhs = SolverExpression(
                        sub_expressions=[self.rhs, sub_expression], operand="sub"
                    )
                    (
                        info_logger.info(
                            f"Switched '+ {sub_expression.value}' from the left to the right side"
                        )
                        if include_original_operand
                        else info_logger.info(
                            f"Switched '{sub_expression.value}' from the left to the right side"
                        )
                    )
                elif original_operand == "sub":
                    self.rhs = SolverExpression(
                        sub_expressions=[self.rhs, sub_expression], operand="add"
                    )
                    (
                        info_logger.info(
                            f"Switched '- {sub_expression.value}' from the left to the right side"
                        )
                        if include_original_operand
                        else info_logger.info(
                            f"Switched '{sub_expression.value}' from the left to the right side"
                        )
                    )
                elif original_operand == "mul":
                    self.rhs = SolverExpression(
                        sub_expressions=[self.rhs, sub_expression], operand="div"
                    )
                    (
                        info_logger.info(
                            f"Switched '* {sub_expression.value}' from the left to the right side"
                        )
                        if include_original_operand
                        else info_logger.info(
                            f"Switched '{sub_expression.value}' from the left to the right side"
                        )
                    )
                elif original_operand == "div":
                    self.rhs = SolverExpression(
                        sub_expressions=[self.rhs, sub_expression], operand="mul"
                    )
                    (
                        info_logger.info(
                            f"Switched '/ {sub_expression.value}' from the left to the right side"
                        )
                        if include_original_operand
                        else info_logger.info(
                            f"Switched '{sub_expression.value}' from the left to the right side"
                        )
                    )
                return True
        return False

    def solve(self, variable):
        try:
            info_logger.info("Solving: " + str(self))
            lhs_updated = [True]
            rhs_updated = [True]
            switch_lhs_to_rhs = [True]
            # switch_rhs_to_lhs = True
            lhs_solved = [False]
            rhs_solved = [False]

            sub_equations = [self]

            while any(rhs_updated) or any(lhs_updated) or any(switch_lhs_to_rhs):
                for sub_equation_index, sub_equation in enumerate(sub_equations):
                    single_rhs_solved, single_rhs_updated, single_rhs_has_var, _, single_new_rhs_exp = sub_equation.rhs.reduce(
                        sub_equation
                    )
                    if single_rhs_updated:
                        sub_equation.rhs = single_new_rhs_exp
                        info_logger.info("Current form: " + str(sub_equation))

                    single_lhs_solved, single_lhs_updated, single_lhs_has_var, _, single_new_lhs_exp = sub_equation.lhs.reduce(
                        sub_equation
                    )
                    if single_lhs_updated:
                        sub_equation.lhs = single_new_lhs_exp
                        info_logger.info("Current form: " + str(sub_equation))

                    single_switch_lhs_to_rhs = sub_equation.switch_left_to_right()
                    if single_switch_lhs_to_rhs:
                        info_logger.info("Current form: " + str(sub_equation))

                    rhs_updated[sub_equation_index] = single_rhs_updated
                    lhs_updated[sub_equation_index] = single_lhs_updated
                    switch_lhs_to_rhs[sub_equation_index] = single_switch_lhs_to_rhs
                    rhs_solved[sub_equation_index] = single_rhs_solved
                    lhs_solved[sub_equation_index] = single_lhs_solved

            if (
                all(rhs_solved)
                and all(lhs_solved)
                and all([isinstance(sub_equation.lhs, SolverVariable) for sub_equation in sub_equations])
                and all([isinstance(sub_equation.rhs, SolverConstant) for sub_equation in sub_equations])
            ):
                new_variable = SolverVariable(variable.name)
                new_variable.value = [sub_equation.rhs.value for sub_equation in sub_equations]
                info_logger.info("\n")

            else:
                raise Exception("Could not solve equation")

            return new_variable

        except Exception as e:
            _, _, exception_traceback = sys.exc_info()
            file_name = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[
                1
            ]
            error_logger.critical(f"{e}, {file_name}, {exception_traceback.tb_lineno}")

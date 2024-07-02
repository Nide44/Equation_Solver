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
            lhs_updated = True
            rhs_updated = True
            switch_lhs_to_rhs = True
            # switch_rhs_to_lhs = True
            lhs_solved = False
            rhs_solved = False

            while rhs_updated or lhs_updated or switch_lhs_to_rhs:
                rhs_solved, rhs_updated, rhs_has_var, _, new_rhs_exp = self.rhs.reduce(
                    self
                )
                if rhs_updated:
                    self.rhs = new_rhs_exp
                    info_logger.info("Current form: " + str(self))

                lhs_solved, lhs_updated, lhs_has_var, _, new_lhs_exp = self.lhs.reduce(
                    self
                )
                if lhs_updated:
                    self.lhs = new_lhs_exp
                    info_logger.info("Current form: " + str(self))

                switch_lhs_to_rhs = self.switch_left_to_right()
                if switch_lhs_to_rhs:
                    info_logger.info("Current form: " + str(self))

            if (
                rhs_solved
                and lhs_solved
                and isinstance(self.lhs, SolverVariable)
                and isinstance(self.rhs, SolverConstant)
            ):
                new_variable = SolverVariable(variable.name)
                new_variable.value = self.rhs.value
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

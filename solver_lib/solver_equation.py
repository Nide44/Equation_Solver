import sys, os

from solver_lib.logger import error_logger, info_logger
from solver_lib.solver_variable import SolverVariable


class SolverEquation:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str(self.lhs) + " = " + str(self.rhs)

    def solve(self, variable):
        try:
            info_logger.info("Solving: " + str(self))

            rhs_solved, rhs_updated, rhs_has_var, _, new_rhs_exp = self.rhs.reduce(self)
            if rhs_updated:
                self.rhs = new_rhs_exp
                info_logger.info("Current form: " + str(self))

            lhs_solved, lhs_updated, lhs_has_var, _, new_lhs_exp = self.lhs.reduce(self)
            if lhs_updated:
                self.lhs = new_lhs_exp
                info_logger.info("Current form: " + str(self))

            if rhs_solved and lhs_solved and not rhs_has_var and lhs_has_var:
                new_variable = SolverVariable(variable.name)
                new_variable.value = self.rhs.value
                info_logger.info("\n")

                return new_variable

        except Exception as e:
            _, _, exception_traceback = sys.exc_info()
            file_name = os.path.split(exception_traceback.tb_frame.f_code.co_filename)[
                1
            ]
            error_logger.critical(f"{e}, {file_name}, {exception_traceback.tb_lineno}")

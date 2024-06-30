from solver_lib.logger import info_logger

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
    
    def __mul__(self, other):
        return SolverExpression(sub_expressions=[self, other], operand="mul")
    
    def __truediv__(self, other):
        return SolverExpression(sub_expressions=[self, other], operand="div")

    def __str__(self):
        if self.operand == "add":
            return " + ".join(
                [str(subexpression) for subexpression in self.sub_expressions]
            )

        elif self.operand == "sub":
            return " - ".join(
                [str(subexpression) for subexpression in self.sub_expressions]
            )
        
        elif self.operand == "mul":
            return " * ".join(
                [str(subexpression) for subexpression in self.sub_expressions]
            )
        
        elif self.operand == "div":
            return " / ".join(
                [str(subexpression) for subexpression in self.sub_expressions]
            )

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

        if all(sub_exp_solved_list):
            if not any(sub_exp_var_list):
                value1 = sub_exp_value_list[0]
                value2 = sub_exp_value_list[1]
                if self.operand == "add":
                    add_value = value1 + value2
                    info_logger.info(f"Added {value1} and {value2} to get {add_value}")
                    
                    return True, True, False, add_value, type(self.sub_expressions[-1])(add_value)
                
                elif self.operand == "sub":
                    sub_value = value1 - value2
                    info_logger.info(
                        f"Subtracted {value2} from {value1} to get {sub_value}"
                    )
                    return True, True, False, sub_value, type(self.sub_expressions[-1])(sub_value)
                
                elif self.operand == "mul":
                    mul_value = value1 * value2
                    info_logger.info(
                        f"Multiplied {value1} with {value2} to get {mul_value}"
                    )
                    return True, True, False, mul_value, type(self.sub_expressions[-1])(mul_value)
                
                elif self.operand == "div":
                    div_value = value1 / value2
                    info_logger.info(
                        f"Divided {value1} by {value2} to get {div_value}"
                    )
                    return True, True, False, div_value, type(self.sub_expressions[-1])(div_value)
            else:
                pass

        else:
            pass

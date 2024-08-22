from app.lexer.base import TokenSpecification
from app.parser.base import ParsedData


class Executor:
    def __init__(self):
        self.variables = {}

    def execute(self, parsed_data: ParsedData) -> str:
        result = self._evaluate_rpn(parsed_data.rpn)

        if parsed_data.variables_to_set:
            self.variables[parsed_data.variables_to_set.value] = result
            result = f'{parsed_data.variables_to_set.value} = {result}'

        return result

    def _evaluate_rpn(self, rpn):
        stack = []

        for token in rpn:
            if token.type == TokenSpecification.NUMBER.name:
                stack.append(float(token.value))
            elif token.type == TokenSpecification.IDENTIFIER.name:
                if token.value in self.variables:
                    stack.append(self.variables[token.value])
                else:
                    raise ValueError(f"Variable '{token.value}' is not defined.")
            elif token.type == TokenSpecification.OPERATOR.name:
                right = stack.pop()
                left = stack.pop()
                result = self._apply_operator(left, right, token.value)
                stack.append(result)
            elif token.type == TokenSpecification.FUNCTION.name:
                arg = stack.pop()
                result = self._apply_function(arg, token.value)
                stack.append(result)

        return stack.pop()

    @staticmethod
    def _apply_operator(left: int | float, right: int | float, operator):
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if right == 0:
                raise ValueError("Division by zero.")
            return left / right
        elif operator == '^':
            return left ** right
        else:
            raise ValueError(f"Unknown operator: {operator}")

    @staticmethod
    def _apply_function(arg: int | float, function: str):
        import math
        method = getattr(math, function, None)
        if method is None:
            raise ValueError(f'Unknown function: {function}')
        return method(arg)

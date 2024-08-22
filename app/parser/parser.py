from app.lexer.base import TokenSpecification, Token
from app.parser.base import BaseParser, ParsedData, ReservedNames


class Parser(BaseParser):

    def parse(self, tokens: list[Token]) -> ParsedData:
        rpn = []
        operators = []
        variables_to_set = ''
        for token in tokens:
            if token.type == TokenSpecification.IDENTIFIER.name or token.type == TokenSpecification.NUMBER.name:
                if token.type == TokenSpecification.IDENTIFIER.name:
                    if token.value in ReservedNames:
                        raise SyntaxError(f'Unknown identifier: {token.value}')
                rpn.append(token)
            elif token.type == TokenSpecification.NUMBER.name:
                rpn.append(token)
            elif token.type == TokenSpecification.EQUAL.name:
                if variables_to_set:
                    raise SyntaxError('Multiple assignment is not supported')
                if len(rpn) != 1:
                    raise SyntaxError('Invalid assignment')
                variables_to_set = rpn.pop()
            elif token.type == TokenSpecification.OPERATOR.name or token.type == TokenSpecification.FUNCTION.name:
                if token.type == TokenSpecification.FUNCTION.name:
                    if token.value not in ReservedNames:
                        raise SyntaxError(f'Unknown function: {token.value}')
                while operators and self.operator_priority(operators[-1].value) >= self.operator_priority(token.value):
                    rpn.append(operators.pop())
                operators.append(token)
            elif token.type == TokenSpecification.LPARENTHESIS.name:
                operators.append(token)
            elif token.type == TokenSpecification.RPARENTHESIS.name:
                if not operators or TokenSpecification.LPARENTHESIS.name not in [token.type for token in operators]:
                    raise SyntaxError('Closed parenthesis without open parenthesis')
                while operators and operators[-1].value != '(':
                    rpn.append(operators.pop())
                operators.pop()
        while operators:
            if operators[-1].value == '(':
                raise SyntaxError('Open parenthesis without closed parenthesis')
            rpn.append(operators.pop())
        return ParsedData(rpn, variables_to_set)

    @staticmethod
    def operator_priority(operator):
        priority_map = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '^': 3,
            'sin': 3,
            'cos': 3,
            'tan': 3,
            'log': 3,
            'sqrt': 3,
            'exp': 3,
        }
        return priority_map.get(operator, 0)

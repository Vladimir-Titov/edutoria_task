import re

from app.lexer.base import BaseLexer, TokenSpecification, Token


class Lexer(BaseLexer):
    def get_tokens(self, expression: str) -> list[Token]:
        tokens = []
        token_matcher = TokenSpecification.get_token_matcher()
        position = 0
        while position < len(expression):
            match = token_matcher(expression, position)
            if match is not None:
                token_type = match.lastgroup
                value = match.group(token_type)
                if token_type == TokenSpecification.IDENTIFIER.name:
                    function_match = re.match(TokenSpecification.FUNCTION.value, value)
                    if function_match:
                        token_type = TokenSpecification.FUNCTION.name

                if token_type != TokenSpecification.SKIP.name:
                    if token_type == TokenSpecification.NUMBER.name:
                        if '.' in value and value[0] != '.':
                            value = float(value)
                        else:
                            value = int(value)
                    tokens.append(Token(token_type, value))
                position = match.end()
            else:
                raise SyntaxError(f'Unsupported token: {expression[position]}')
        return tokens

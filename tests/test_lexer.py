import pytest

from app.lexer.base import TokenSpecification
from app.lexer.lexer import Lexer


class TestLexer:

    @pytest.fixture
    def lexer(self):
        return Lexer()

    @pytest.mark.parametrize(
        'expression, expected_tokens',
        [
            ('x=3', [
                (TokenSpecification.IDENTIFIER.name, 'x'),
                (TokenSpecification.EQUAL.name, '='),
                (TokenSpecification.NUMBER.name, 3),
            ]),
            ('result= x + sqrt(25)', [
                (TokenSpecification.IDENTIFIER.name, 'result'),
                (TokenSpecification.EQUAL.name, '='),
                (TokenSpecification.IDENTIFIER.name, 'x'),
                (TokenSpecification.OPERATOR.name, '+'),
                (TokenSpecification.FUNCTION.name, 'sqrt'),
                (TokenSpecification.LPARENTHESIS.name, '('),
                (TokenSpecification.NUMBER.name, 25),
                (TokenSpecification.RPARENTHESIS.name, ')'),
            ]),
            ('z=sin(s)+ cos(25)', [
                (TokenSpecification.IDENTIFIER.name, 'z'),
                (TokenSpecification.EQUAL.name, '='),
                (TokenSpecification.FUNCTION.name, 'sin'),
                (TokenSpecification.LPARENTHESIS.name, '('),
                (TokenSpecification.IDENTIFIER.name, 's'),
                (TokenSpecification.RPARENTHESIS.name, ')'),
                (TokenSpecification.OPERATOR.name, '+'),
                (TokenSpecification.FUNCTION.name, 'cos'),
                (TokenSpecification.LPARENTHESIS.name, '('),
                (TokenSpecification.NUMBER.name, 25),
                (TokenSpecification.RPARENTHESIS.name, ')'),
            ]),
            ('', []),
        ]
    )
    def test_get_tokens(self, expression, expected_tokens, lexer):
        tokens = lexer.get_tokens(expression)
        assert tokens == expected_tokens

    @pytest.mark.parametrize(
        'expression, expected_error_message',
        [
            ('a + b @ c', 'Unsupported token: @'),
        ]
    )
    def test_unexpected_character(self, expression, expected_error_message, lexer):
        with pytest.raises(SyntaxError, match=expected_error_message):
            lexer.get_tokens(expression)

import pytest

from app.lexer.base import TokenSpecification, Token
from app.lexer.lexer import Lexer
from app.parser import Parser


class TestParser:

    @pytest.mark.parametrize(
        'input_expression, expected_rpn, expected_variable', [
            (
                'result = (3 + 4) * 5',
                [
                    Token(type=TokenSpecification.NUMBER.name, value=3),
                    Token(type=TokenSpecification.NUMBER.name, value=4),
                    Token(type=TokenSpecification.OPERATOR.name, value='+'),
                    Token(type=TokenSpecification.NUMBER.name, value=5),
                    Token(type=TokenSpecification.OPERATOR.name, value='*'),
                ],
                'result'
            ),
            (
                'x = 5 + 3 * (2 - 1)',
                [
                    Token(type=TokenSpecification.NUMBER.name, value=5),
                    Token(type=TokenSpecification.NUMBER.name, value=3),
                    Token(type=TokenSpecification.NUMBER.name, value=2),
                    Token(type=TokenSpecification.NUMBER.name, value=1),
                    Token(type=TokenSpecification.OPERATOR.name, value='-'),
                    Token(type=TokenSpecification.OPERATOR.name, value='*'),
                    Token(type=TokenSpecification.OPERATOR.name, value='+'),
                ],
                'x'
            ),
            (
                'y123 = sin(a) + 4',
                [
                    Token(type=TokenSpecification.IDENTIFIER.name, value='a'),
                    Token(type=TokenSpecification.FUNCTION.name, value='sin'),
                    Token(type=TokenSpecification.NUMBER.name, value=4),
                    Token(type=TokenSpecification.OPERATOR.name, value='+'),
                ],
                'y123'
            ),
            (
                'result = (3 + 4) * 5 * (2 + 3)',
                [
                    Token(type=TokenSpecification.NUMBER.name, value=3),
                    Token(type=TokenSpecification.NUMBER.name, value=4),
                    Token(type=TokenSpecification.OPERATOR.name, value='+'),
                    Token(type=TokenSpecification.NUMBER.name, value=5),
                    Token(type=TokenSpecification.OPERATOR.name, value='*'),
                    Token(type=TokenSpecification.NUMBER.name, value=2),
                    Token(type=TokenSpecification.NUMBER.name, value=3),
                    Token(type=TokenSpecification.OPERATOR.name, value='+'),
                    Token(type=TokenSpecification.OPERATOR.name, value='*'),
                ],
                'result'
            ),
        ])
    def test_parser(self, input_expression, expected_rpn, expected_variable):
        tokens = Lexer().get_tokens(input_expression)
        parser = Parser()

        parsed_data = parser.parse(tokens)

        assert len(parsed_data.rpn) == len(expected_rpn)
        for expected_token, actual_token in zip(expected_rpn, parsed_data.rpn):
            assert expected_token.type == actual_token.type
            assert expected_token.value == actual_token.value

        assert parsed_data.variables_to_set.value == expected_variable

    def test_parser_invalid_expression(self):
        tokens = Lexer().get_tokens('result = 3 + (4 * 5')
        parser = Parser()

        with pytest.raises(SyntaxError, match='Open parenthesis without closed parenthesis'):
            parser.parse(tokens)

    def test_parser_multiple_assignment(self):
        tokens = Lexer().get_tokens('result1 = 5 result2 = 6')
        parser = Parser()

        with pytest.raises(SyntaxError, match='Multiple assignment is not supported'):
            parser.parse(tokens)

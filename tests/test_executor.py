import pytest

from app.executor import Executor
from app.lexer.base import TokenSpecification, Token
from app.parser.base import ParsedData


class TestExecutor:

    def setup_method(self):
        self.executor = Executor()

    @pytest.mark.parametrize(
        'rpn, expected_result',
        [
            ([
                 Token(type=TokenSpecification.NUMBER.name, value=3),
                 Token(type=TokenSpecification.NUMBER.name, value=4),
                 Token(type=TokenSpecification.OPERATOR.name, value='+')
             ], 7),
            ([
                 Token(type=TokenSpecification.NUMBER.name, value=10),
                 Token(type=TokenSpecification.NUMBER.name, value=5),
                 Token(type=TokenSpecification.OPERATOR.name, value='-')
             ], 5),
            ([
                 Token(type=TokenSpecification.NUMBER.name, value=3),
                 Token(type=TokenSpecification.NUMBER.name, value=4),
                 Token(type=TokenSpecification.OPERATOR.name, value='*')
             ], 12),
            ([
                 Token(type=TokenSpecification.NUMBER.name, value=20),
                 Token(type=TokenSpecification.NUMBER.name, value=4),
                 Token(type=TokenSpecification.OPERATOR.name, value='/')
             ], 5),
        ]
    )
    def test_execute_simple_operations(self, rpn, expected_result):
        parsed_data = ParsedData(rpn=rpn, variables_to_set=None)
        result = self.executor.execute(parsed_data)
        assert result == expected_result

    def test_execute_with_variable_assignment(self):
        rpn = [
            Token(type=TokenSpecification.NUMBER.name, value=2),
            Token(type=TokenSpecification.NUMBER.name, value=3),
            Token(type=TokenSpecification.OPERATOR.name, value='+')
        ]
        parsed_data = ParsedData(
            rpn=rpn,
            variables_to_set=Token(type=TokenSpecification.IDENTIFIER.name, value='result')
        )
        result = self.executor.execute(parsed_data)

        assert result == 'result = 5.0'
        assert self.executor.variables['result'] == 5

    def test_execute_with_variable_usage(self):
        self.executor.variables['a'] = 2
        rpn = [
            Token(type=TokenSpecification.IDENTIFIER.name, value='a'),
            Token(type=TokenSpecification.NUMBER.name, value=3),
            Token(type=TokenSpecification.OPERATOR.name, value='+')
        ]
        parsed_data = ParsedData(rpn=rpn, variables_to_set=None)
        result = self.executor.execute(parsed_data)

        assert result == 5

    def test_execute_with_undefined_variable(self):
        rpn = [
            Token(type=TokenSpecification.IDENTIFIER.name, value='undefined_var'),
            Token(type=TokenSpecification.NUMBER.name, value=3),
            Token(type=TokenSpecification.OPERATOR.name, value='+')
        ]
        parsed_data = ParsedData(rpn=rpn, variables_to_set=None)

        with pytest.raises(ValueError, match="Variable 'undefined_var' is not defined."):
            self.executor.execute(parsed_data)

    def test_execute_with_division_by_zero(self):
        rpn = [
            Token(type=TokenSpecification.NUMBER.name, value=10),
            Token(type=TokenSpecification.NUMBER.name, value=0),
            Token(type=TokenSpecification.OPERATOR.name, value='/')
        ]
        parsed_data = ParsedData(rpn=rpn, variables_to_set=None)

        with pytest.raises(ValueError, match="Division by zero."):
            self.executor.execute(parsed_data)

    def test_execute_with_unknown_operator(self):
        rpn = [
            Token(type=TokenSpecification.NUMBER.name, value=10),
            Token(type=TokenSpecification.NUMBER.name, value=5),
            Token(type=TokenSpecification.OPERATOR.name, value='?')
        ]
        parsed_data = ParsedData(rpn=rpn, variables_to_set=None)

        with pytest.raises(ValueError, match="Unknown operator: ?"):
            self.executor.execute(parsed_data)

    def test_execute_with_unknown_function(self):
        rpn = [
            Token(type=TokenSpecification.NUMBER.name, value=10),
            Token(type=TokenSpecification.FUNCTION.name, value='unknown_function')
        ]
        parsed_data = ParsedData(rpn=rpn, variables_to_set=None)

        with pytest.raises(ValueError, match='Unknown function: unknown_function'):
            self.executor.execute(parsed_data)

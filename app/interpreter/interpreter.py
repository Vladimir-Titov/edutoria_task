from app.executor import Executor
from app.lexer import Lexer
from app.parser import Parser


class Interpreter:

    def __init__(self):
        self.parser = Parser()
        self.lexer = Lexer()
        self.executor = Executor()

    def execute(self, expression: str) -> str:
        tokens = self.lexer.get_tokens(expression)
        parsed_data = self.parser.parse(tokens)
        return self.executor.execute(parsed_data)

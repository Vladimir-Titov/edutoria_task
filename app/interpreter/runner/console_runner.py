from app.interpreter.interpreter import Interpreter
from app.interpreter.runner.base import BaseRunner


class ConsoleRunner(BaseRunner):

    def __init__(self, invite_line: str):
        self.invite_line = invite_line

    def run(self, interpreter: Interpreter) -> str:
        while True:
            try:
                expression = input(self.invite_line)
                result = interpreter.execute(expression)
                print(result)
            except KeyboardInterrupt:
                break
            except Exception as exc:
                print(f'Error: {exc}')
        print('Bye!')

from app.interpreter.interpreter import Interpreter
from app.interpreter.runner.console_runner import ConsoleRunner


def main():
    runner = ConsoleRunner('>>> ')
    interpreter = Interpreter()

    runner.run(interpreter)


if __name__ == '__main__':
    main()

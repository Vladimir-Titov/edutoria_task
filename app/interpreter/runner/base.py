from abc import ABC, abstractmethod

from app.interpreter.interpreter import Interpreter


class BaseRunner(ABC):

    @abstractmethod
    def run(self, interpreter: Interpreter) -> str:
        pass

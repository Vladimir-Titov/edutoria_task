from abc import ABC
from collections import namedtuple

from app.lexer.base import Token

ParsedData = namedtuple('ParsedData', 'rpn variables_to_set')

ReservedNames = [
    'sin',
    'cos',
    'tan',
    'log',
    'sqrt',
    'exp',
]


class BaseParser(ABC):

    def parse(self, tokens: list[Token]) -> ParsedData:
        raise NotImplementedError

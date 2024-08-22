import re
from abc import ABC, abstractmethod
from collections import namedtuple
from enum import Enum

Token = namedtuple('Token', 'type value')


class TokenSpecification(Enum):
    NUMBER = r'\b\d+(\.\d*)?\b'
    IDENTIFIER = r'\b[a-zA-Z_]\w*\b'
    OPERATOR = r'[+\-*/^]'
    LPARENTHESIS = r'\('
    RPARENTHESIS = r'\)'
    FUNCTION = r'\b(sin|cos|tan|log|sqrt|exp)\b'
    EQUAL = r'='
    SKIP = r'\s+'

    @classmethod
    def get_token_matcher(cls):
        regex = '|'.join(f'(?P<{elem.name}>{elem.value})' for elem in cls if elem.name != cls.FUNCTION.name)
        return re.compile(regex).match


class BaseLexer(ABC):

    @abstractmethod
    def get_tokens(self, expression: str) -> list[str]:
        raise NotImplementedError

from __future__ import annotations
from abc import ABC
import re
from enum import Enum
from typing import List


alphabet = re.compile(r"[a-z]", re.I)

numbers = re.compile(r"[0-9]")

whitespace = re.compile(r"\s")

# Source: https://www.programiz.com/c-programming/list-all-keywords-c-language
keywords = ["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", "extern", "float", "for", "goto", "if",
            "int", "long", "register", "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"]

specials = ['(', ')', '{', '}', '[', ']', '\\', '\'', '"', ':', ';']

operators = ['+', '-', '/', '*', '%', '<', '=', '>', '!', '~', '^', '|', '&']


class SyntaxKind(Enum):
    # TOKEN TYPES
    EOF = 1
    SPACE = 2
    OPERATOR = 3
    SPECIAL = 4
    KEYWORD = 5
    IDENTIFIER = 6
    NUMBER = 7
    BAD = 8
    # EXPRESSIONS
    NumberExpression = 9
    BinaryExpression = 10
    ParenthesizedExpression = 11


class Node(ABC):
    kind: SyntaxKind
    children: List[Node]


class Token(Node):
    value: str | float | None
    position: int

    def __init__(self, type: SyntaxKind, value: str | float | None, position: int) -> None:
        super().__init__()
        self.kind = type
        self.value = value
        self.position = position
        self.children = []


class ExpressionNode(Node, ABC):
    def __init__(self) -> None:
        super().__init__()


def isNum(char: str) -> bool:
    return True if re.match(numbers, char) else False  # type: ignore


def isAlpha(char: str) -> bool:
    return True if re.match(alphabet, char) else False


def isSpace(char: str) -> bool:
    return True if re.match(whitespace, char) else False


def isAlnum(char: str) -> bool:
    return True if isAlpha(char) or isNum(char) else False


def isKeyword(string: str) -> bool:
    return True if string in keywords else False


def isSpecial(char: str) -> bool:
    return True if char in specials else False


def isOperator(char: str) -> bool:
    return True if char in operators else False

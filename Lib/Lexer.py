from Utils.Identifiers import *
from Utils.Casting import *


class Lexer:
    input: str
    input_size: int

    position: int = 0
    current: str

    diagnostics: List[str] = []

    def __init__(self, input: str):
        self.input = input
        self.input_size = len(input) - 1

    def nextChar(self):
        self.position += 1

    def currentChar(self):
        return self.input[self.position] if self.position <= self.input_size else ''

    def nextToken(self):
        if self.position > self.input_size:
            self.nextChar()
            return Token(type=SyntaxKind.EOF, value=None, position=self.position)

        if (isSpace(self.currentChar())):
            self.nextChar()
            return Token(type=SyntaxKind.SPACE, value=None, position=self.position)

        if (isOperator(self.currentChar())):
            value = self.currentChar()
            self.nextChar()
            return Token(type=SyntaxKind.OPERATOR, value=value, position=self.position)

        if (isSpecial(self.currentChar())):
            value = self.currentChar()
            self.nextChar()
            return Token(type=SyntaxKind.SPECIAL, value=value, position=self.position)

        if (isAlpha(self.currentChar())):
            valueStr: str = ""
            start = self.position
            while (isAlnum(self.currentChar())):
                valueStr += self.currentChar()
                self.nextChar()

            if (isKeyword(valueStr)):
                self.nextChar()
                return Token(type=SyntaxKind.KEYWORD, value=valueStr, position=start)

            self.nextChar()
            return Token(type=SyntaxKind.IDENTIFIER, value=valueStr, position=start)

        if (isNum(self.currentChar()) or self.currentChar() == '.'):
            numStr: str = ""
            start = self.position
            while isNum(self.currentChar()) or self.currentChar() == '.' or self.currentChar() == '\'' and self.position < self.input_size:
                numStr += self.currentChar() if self.currentChar() != '\'' else ""
                self.nextChar()
            floatValue = strToFloat(numStr)
            return Token(type=SyntaxKind.NUMBER, value=floatValue, position=start)

        self.diagnostics.append(
            f"ERROR: bad character input: '{self.currentChar()}'")
        return Token(type=SyntaxKind.BAD, value=None, position=self.position)

from Lib.Lexer import Lexer, Token
from Utils.Identifiers import SyntaxKind, ExpressionNode

from typing import List


class NumberExpressionNode(ExpressionNode):
    token: Token

    def __init__(self, numberToken: Token) -> None:
        super().__init__()
        self.kind = SyntaxKind.NumberExpression
        self.token = numberToken

        self.children = [numberToken]


class BinaryExpressionNode(ExpressionNode):
    left: ExpressionNode
    operator: Token
    right: ExpressionNode

    def __init__(self, left: ExpressionNode, operator: Token, right: ExpressionNode) -> None:
        super().__init__()
        self.kind = SyntaxKind.BinaryExpression
        self.left = left
        self.operator = operator
        self.right = right

        self.children = [self.left, self.operator, self.right]


class ParenthesizedExpressionSyntax(ExpressionNode):
    openParenToken: Token
    expression: ExpressionNode
    closeParenToken: Token

    def __init__(self, openParenToken: Token, expression: ExpressionNode, closeParenToken: Token):
        super().__init__()
        self.kind = SyntaxKind.ParenthesizedExpression
        self.openParenToken = openParenToken
        self.expression = expression
        self.closeParenToken = closeParenToken

        self.children = [self.openParenToken,
                         self.expression, self.closeParenToken]


class Parser:
    tokens: List[Token] = []

    _position: int = 0

    diagnostics: List[str]

    def __init__(self, text) -> None:
        lexer = Lexer(text)
        while True:
            token = lexer.nextToken()
            if (token.kind == SyntaxKind.EOF or token.kind == SyntaxKind.BAD):
                break
            if (not token.kind == SyntaxKind.SPACE):
                self.tokens.append(token)
        self.diagnostics = lexer.diagnostics

    def peek(self, offset: int) -> Token:
        index = self._position + offset
        if (index >= len(self.tokens)):
            return self.tokens[len(self.tokens) - 1]
        return self.tokens[index]

    def current(self) -> Token: return self.peek(0)

    def nextToken(self) -> Token:
        current = self.current()
        self._position += 1
        return current

    def match(self, kind: SyntaxKind) -> Token:
        if (self.current().kind == kind):
            return self.nextToken()
        self.diagnostics.append(
            f"ERROR: Unexpected token <{self.current().kind}>, expected <{kind}>")

        return Token(type=kind, value=None, position=self.current().position)

    def parsePrimaryExpression(self) -> ExpressionNode:

        if (self.current().kind == SyntaxKind.SPECIAL and self.current().value == "("):
            left = self.nextToken()
            expression = self.parseTerm()
            # TODO: Change this to Paren token
            right = self.match(SyntaxKind.SPECIAL)
            return ParenthesizedExpressionSyntax(openParenToken=left, expression=expression, closeParenToken=right)

        numberToken = self.match(SyntaxKind.NUMBER)
        return NumberExpressionNode(numberToken)

    def parseTerm(self) -> ExpressionNode:
        left = self.parseFactor()
        while (self.current().kind == SyntaxKind.OPERATOR and self.current().value == "+" or self.current().value == "-"):
            operatorToken = self.nextToken()
            right = self.parseFactor()
            left = BinaryExpressionNode(left, operatorToken, right)
        return left

    def parseFactor(self) -> ExpressionNode:
        left = self.parsePrimaryExpression()
        while (self.current().kind == SyntaxKind.OPERATOR and self.current().value == "*" or self.current().value == "/"):
            operatorToken = self.nextToken()
            right = self.parsePrimaryExpression()
            left = BinaryExpressionNode(left, operatorToken, right)
        return left


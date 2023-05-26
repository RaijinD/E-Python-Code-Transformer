from Utils.PrettyPrint import PrettyPrint
from Lib.Parser import Parser



def DriverLoop(text: str):
    parser = Parser(text)
    expr = parser.parseTerm()
    PrettyPrint(expr)
    if (parser.diagnostics):
        for diagnostic in parser.diagnostics:
            print(diagnostic)

from lexer import Lexer, TokenType, LexerToken
from parser.parser import Parser
from parser.node import AstNode, NodeType
from parser.source_location import SourceLocation
from interpreter.interpreter import Interpreter
from error import InterpreterError
from ast_printer import AstPrinter

class Repl:
    REPL_FILENAME = '<repl>'

    def __init__(self):
        self.interpreter = Interpreter(SourceLocation(Repl.REPL_FILENAME))

    def loop(self):
        while True:
            self.accept_input()

    def accept_input(self):
        line = input('>>> ')

        (line_ast, error_list) = self.parse_line(line)

        # for node in line_ast:
        #     AstPrinter().print_ast(node)

        if len(error_list.errors) > 0:
            error_list.print_errors()
            return

        for node in line_ast:
            try:
                self.interpreter.visit(node)
            except InterpreterError:
                continue

    def parse_line(self, line):
        lexer = Lexer(line, SourceLocation(Repl.REPL_FILENAME))
        lexer.lex()

        parser = Parser(lexer)
        return (parser.parse(), parser.error_list)

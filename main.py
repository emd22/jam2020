#!/bin/python3

from lexer import Lexer, TokenType, LexerToken
from parser.parser import Parser 
from parser.node import NodeImport
from parser.source_location import SourceLocation
from interpreter.interpreter import Interpreter
from error import InterpreterError

from repl.repl import Repl
from ast_printer import AstPrinter

import sys

def main():
    if len(sys.argv) <= 1:
        repl = Repl()
        repl.loop()
        return
    
    filename = sys.argv[1]
    
    try:
        fp = open(filename, 'r')
    except FileNotFoundError:
        print('Script \'{}\' could not be found'.format(filename))
        
    data = fp.read()

    lexer = Lexer(data, SourceLocation(filename))
    lexer.lex()

    parser = Parser(lexer)
    
    # all files include the __core__ file which contains internal types and methods
    global_import_nodes = [
        parser.import_file('std/__core__.peach')
    ]
    
    # import nodes should be located at top of tree
    ast = global_import_nodes+parser.parse()

    # for node in ast:
    #    AstPrinter().print_ast(node)

    error_list = parser.error_list

    if len(error_list.errors) > 0:
        error_list.print_errors()
        return

    # init interpreter and parse tokens
    interpreter = Interpreter(parser.source_location)
    
    print("=== Output ===")

    try:
        for node in ast:
            interpreter.visit(node)
    except InterpreterError:
        # errors printed
        interpreter.error_list.clear_errors()

if __name__ == '__main__':
    main()

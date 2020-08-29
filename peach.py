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


class Peach():
    def __init__(self):
        pass

    def eval(self, data=None, filename=None, interpret=True, default_imports=['std/__core__.peach']):
        debug_name = "<none>"

        if filename != None:
            try:
                self.file = open(filename, 'r')
            except FileNotFoundError:
                print("Script '{}' could not be found".format(filename))
                return None
            debug_name = filename
            self.data = self.file.read()
        
        elif data != None:
            self.data = data
        
        else:
            self.data = ""

        self.lexer = Lexer(self.data, SourceLocation(debug_name))
        self.parser = Parser(self.lexer.lex(), self.lexer.source_location)
        # all default imports should be here
        global_import_nodes = []
        for path in default_imports:
            global_import_nodes.append(self.parser.import_file(path))
        # combine global imports and parser ast    
        self.ast = global_import_nodes+self.parser.parse()
        error_list = self.parser.error_list

        if len(error_list.errors) > 0:
            error_list.print_errors()
            return

        return_code = None
        if interpret:

            # init interpreter and visit nodes
            self.interpreter = Interpreter(self.parser.source_location)

            try:
                for node in self.ast:
                    return_code = self.interpreter.visit(node)
            except InterpreterError:
                # errors printed in interpreter
                self.interpreter.error_list.clear_errors()
        return return_code

    def eval_file(self, filename):
        return self.eval(filename=filename)
    def eval_data(self, data):
        return self.eval(data=data)
        
    def call_function(self, function_name, arguments=[]):
        if self.interpreter == None:
            raise Exception("Peach not initialized! please run ")
        if type(arguments) != list:
            raise Exception("Arguments type is not list!")

        return self.interpreter.call_function(function_name, arguments)

    def repl(self):
        repl = Repl()
        repl.loop()
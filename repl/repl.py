from lexer import Lexer, TokenType, LexerToken
from parser.parser import Parser
from parser.node import AstNode, NodeType
from parser.source_location import SourceLocation
from interpreter.interpreter import Interpreter
from interpreter.env.builtins import obj_to_string
from error import InterpreterError
from ast_printer import AstPrinter
from util import LogColour

# when including readline, it switches input() over and allows
# text seeking and other cool things
import readline

import signal

class Repl:
    REPL_FILENAME = '<repl>'

    def __init__(self):
        self._walkthrough_messages = self.load_walkthrough_messages()

        self.welcome_message = """
            ----- P E A C H -----

        Let's get started!
        To learn more about PEACH,
        type one of the following:

  {}
            """.format('\n  '.join(map(lambda key: "{}--  {}".format(key.ljust(16), self._walkthrough_messages[key][0]), self._walkthrough_messages)))


        self.interpreter = Interpreter(SourceLocation(Repl.REPL_FILENAME))
        
        print(self.welcome_message)
                
        self.repl_import_defaults()

        signal.signal(signal.SIGINT, self.at_exit)
        
    def at_exit(self, signal, frame):
        print('\nExiting...')
        exit(0)
        
    def repl_import_defaults(self):

        # generate import nodes
        repl_import_nodes = [
            Parser.import_file(Parser, 'std/__core__.peach'),
            Parser.import_file(Parser, 'std/__repl__.peach')
        ]

        # eval asts
        self.eval_line_ast(repl_import_nodes)
        
    def loop(self):
        while True:
            self.accept_input()

    def load_walkthrough_content(self, filename):
        file_content = open('./doc/{}'.format(filename)).readlines()

        title = file_content[0:1][0].strip().replace('#', '')
        content = ''.join(file_content[1:]).strip()

        return (title, content)

    def load_walkthrough_messages(self):
        from os import walk, path
        import re

        f = []
        for (dirpath, dirnames, filenames) in walk('./doc'):
            f.extend(filenames)
            break

        walkthrough_messages = {}

        for filename in sorted(f):
            try:
                x = re.search("\d\d_([A-Za-z]*)\.md", filename)
                command_name = x[1]

                walkthrough_messages[command_name] = self.load_walkthrough_content(filename)
            except:
                print("Failed to load documentation file {}".format(filename))

        return walkthrough_messages

    def accept_input(self):
        line = ""
        
        line = input('>>> ')

        trimmed = line.strip()
        if trimmed in self._walkthrough_messages:
            print(self._walkthrough_messages[trimmed][1])

            return

        (brace_counter, bracket_counter, paren_counter) = self.count_continuation_tokens(line)

        while brace_counter > 0 or bracket_counter > 0 or paren_counter > 0:
            next_line = input('... ')
            line += next_line + '\n'
            (brace_counter, bracket_counter, paren_counter) = self.count_continuation_tokens(line)

        (line_ast, error_list) = self.parse_line(line)

        # for node in line_ast:
        #     AstPrinter().print_ast(node)

        if len(error_list.errors) > 0:
            error_list.print_errors()
            return
            
        self.eval_line_ast(line_ast)

    def eval_line_ast(self, line_ast):
        last_value = None
        last_node = None

        for node in line_ast:
            last_node = node
            try:
                last_value = self.interpreter.visit(node)
            except InterpreterError:
                self.interpreter.error_list.clear_errors()
                continue

        if last_value is not None:
            obj_str = obj_to_string(self.interpreter, last_node, last_value)
            print(f"{LogColour.Info}{obj_str}{LogColour.Default}")

    def parse_line(self, line):
        lexer = Lexer(line, SourceLocation(Repl.REPL_FILENAME))
        lexer.lex()

        parser = Parser(lexer)
        
        return (parser.parse(), parser.error_list)

    def count_continuation_tokens(self, line):
        brace_counter = 0
        bracket_counter = 0
        paren_counter = 0

        for ch in line:
            if ch == '{':
                brace_counter += 1
            elif ch == '}':
                brace_counter -= 1
            elif ch == '(':
                paren_counter += 1
            elif ch == ')':
                paren_counter -= 1
            elif ch == '[':
                bracket_counter += 1
            elif ch == ']':
                bracket_counter -= 1

        return (brace_counter, bracket_counter, paren_counter)

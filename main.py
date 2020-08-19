from lexer import Lexer, TokenType, LexerToken
from parser.parser import Parser
from parser.source_location import SourceLocation
from interpreter.interpreter import Interpreter

from repl.repl import Repl
from ast_printer import AstPrinter

def main():
    repl = Repl()
    repl.loop()

    return

    filename = "test.kb"
    data = open(filename, "r").read()

    lexer = Lexer(data, SourceLocation(filename))
    lexer.lex()
    #print_tokens(lexer)
    
    #print_func("=== Parser ===")
    
    parser = Parser(lexer)
    ast = parser.parse()
    error_list = parser.error_list

    if len(error_list.errors) > 0:
        error_list.print_errors()
        return

    # init interpreter and parse tokens
    interpreter = Interpreter(parser.source_location)
    # print them bad boys out
    for node in ast:
        AstPrinter().print_ast(node)
    
    print("=== Output ===")
    for node in ast:
        interpreter.visit(node)

if __name__ == '__main__':
    main()

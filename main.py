from lexer import Lexer, TokenType, LexerToken
from parser import Parser, AstNode, NodeType
from interpreter import Interpreter

def print_tokens(lexer):
    for token in lexer.tokens:
        print(token)

def print_ast(node):
    if node == None:
        return
    
    print(node)
    
    if node.type == NodeType.BinOp:
        # branch left & right
        print_ast(node.left)
        print_ast(node.right)
        

def main():
    data = open("test.kb", "r").read()

    lexer = Lexer(data)
    lexer.lex()
    # gimme some greasy tokens
    print_tokens(lexer)
    
    print("=== Parser shiz ===")
    
    parser = Parser(lexer)
    # init interpreter and parse tokens
    interpreter = Interpreter(parser)
    # print them bad boys out
    print_ast(interpreter.ast)
    
    print(interpreter.interpret())

if __name__ == '__main__':
    main()

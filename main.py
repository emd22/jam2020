from lexer import Lexer, TokenType, LexerToken
from parser.parser import Parser
from parser.node import AstNode, NodeType
from interpreter.interpreter import Interpreter

def print_tokens(lexer):
    for token in lexer.tokens:
        print(token)

def print_ast(node):
    if node == None:
        return
    
    print(node)
    
    if node.type == NodeType.Block:
        for child in node.children:
            print_ast(child)
            
    elif node.type == NodeType.BinOp:
        # branch left & right
        print_ast(node.left)
        print_ast(node.right)
    
    elif node.type == NodeType.Assign:
        print_ast(node.var)
        print_ast(node.value)
        
    elif node.type == NodeType.Declare:
        print_ast(node.value)
        

def main():
    data = open("test.kb", "r").read()

    lexer = Lexer(data)
    lexer.lex()
    print_tokens(lexer)
    
    print("=== Parser ===")
    
    parser = Parser(lexer)
    # init interpreter and parse tokens
    interpreter = Interpreter(parser)
    # print them bad boys out
    print_ast(interpreter.ast)
    
    print("=== Output ===")
    interpreter.interpret()

if __name__ == '__main__':
    main()

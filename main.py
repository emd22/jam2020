from lexer import Lexer, TokenType, LexerToken
from parser.parser import Parser
from parser.node import AstNode, NodeType
from interpreter.interpreter import Interpreter
from interpreter.scope import Variable, VariableType

def print_func(string):
    print(string)

def print_tokens(lexer):
    for token in lexer.tokens:
        print_func(token)

def print_ast(node):
    if node == None:
        return
    
    print_func(node)
    
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
    elif node.type == NodeType.ArgumentList:
        print_func('(')

        for argument in node.arguments:
            print_ast(argument)
            print_func(', ')

        print_func(')')
    elif node.type == NodeType.FunctionExpression:
        print_func('<Function>')
        print_ast(node.argument_list)
        print_ast(node.block)
        

def main():
    filename = "test.kb"
    data = open(filename, "r").read()

    lexer = Lexer(data)
    lexer.lex()
    #print_tokens(lexer)
    
    print_func("=== Parser ===")
    
    parser = Parser(lexer)
    # init interpreter and parse tokens
    interpreter = Interpreter(parser, filename)
    # print them bad boys out
    print_ast(interpreter.ast)
    
    print_func("=== Output ===")
    interpreter.interpret()

if __name__ == '__main__':
    main()

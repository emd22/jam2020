from lexer import Lexer, TokenType, LexerToken
from parser import Parser, AstNode, NodeType

def print_tokens(lexer):
    for token in lexer.tokens:
        print(token)

def print_ast(tnode):
    if tnode == None:
        return
    print(tnode)
    if tnode.type == NodeType.BinOp:
        print_ast(tnode.left)
        print_ast(tnode.right)
        

def main():
    data = open("test.kb", "r").read()

    lexer = Lexer(data)
    lexer.lex()
    print_tokens(lexer)
    parser = Parser(lexer)
    ast = parser.parse()
    print_ast(ast)


if __name__ == '__main__':
    main()

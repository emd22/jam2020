from lexer import LexerToken, TokenType
import enum

class NodeType(enum.Enum):
    BinOp = 1
    Number = 2
    

class AstNode():
    def __init__(self, type, token):
        self.type = type
        self.token = token
    def __str__(self):
        return "AstNode[{0}, {1}]".format(self.type, self.token)
    def __repr__(self):
        return self.__str__()
        
class NodeBinOp(AstNode):
    def __init__(self, left, token, right):
        self.type = NodeType.BinOp
        self.left = left
        self.token = token
        self.right = right
        
class NodeNumber(AstNode):
    def __init__(self, token):
        self.type = NodeType.Number
        self.token = token
        self.value = int(token.value)

class Parser():
    def __init__(self, lexer):
        self.nodes = []
        self.lexer = lexer
        self.token_index = 0
        self.current_token = self.next_token()
    
    def next_token(self):
        #if self.token_index+1 > len(self.lexer.tokens):
        #    raise Exception('Token index out of range')
        self.token_index += 1
        self.current_token = self.lexer.tokens[self.token_index]
        return self.current_token
    
    def error(self):
        raise Exception('Invalid syntax')
    
    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.next_token()
        else:
            print("Error: type {0} != {1}".format(self.current_token.type, type))
            self.error()
    
    def parse_factor(self):
        # handles value or (x ± x)
        token = self.current_token
        
        if token.type == TokenType.Number:
            self.eat(TokenType.Number)
            return NodeNumber(token)
        elif token.type == TokenType.LParen:
            self.eat(TokenType.LParen)
            node = self.parse_expression()
            print("***{0}".format(self.current_token))
            self.eat(TokenType.RParen)
            return node
            
    def parse_term(self):
        # handles multiply, division, expressions
        node = self.parse_factor()
        while self.current_token.type in (TokenType.Multiply, TokenType.Divide):
            token = self.current_token
            if token.type == TokenType.Multiply:
                self.eat(TokenType.Multiply)
            elif token.type == TokenType.Divide:
                self.eat(TokenType.Divide)
            node = NodeBinOp(left=node, token=token, right=self.parse_factor())
        return node
    
    def parse_expression(self):
        node = self.parse_term()
        while self.current_token.type in (TokenType.Plus, TokenType.Minus):
            token = self.current_token
            if token.type == TokenType.Plus:
                self.eat(TokenType.Plus)
            elif token.type == TokenType.Minus:
                self.eat(TokenType.Minus)
            node = NodeBinOp(left=node, token=token, right=self.parse_term())
        return node
        
    def parse(self):
        return self.parse_expression()

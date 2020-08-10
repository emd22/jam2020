from lexer import LexerToken, TokenType
from parser.node import *
# peter parser
    
class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_index = 0
        self.current_token = self.next_token()
    
    def next_token(self):
        #if self.token_index+1 > len(self.lexer.tokens):
        #    raise Exception('Token index out of range')
        self.current_token = self.lexer.tokens[self.token_index]
        self.token_index += 1
        return self.current_token
    
    def error(self, message):
        raise Exception('Syntax error: {}'.format(message))
    
    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.next_token()
        else:
            self.error('expected {0} but recieved {1}'.format(type, self.current_token.type))
    
    def parse_variable(self):
        # create variable node and eat identifier
        node = NodeVariable(self.current_token)
        self.eat(TokenType.Identifier)
        return node
    
    def parse_assignment_statement(self):
        left = self.parse_variable()
        token = self.current_token
        self.eat(TokenType.Equals)
        right = self.expression()
        node = NodeAssign(left, token, right)
        return node
    
    def parse_statement(self):
        token = self.current_token
        if token.type == TokenType.LBrace:
            node = self.parse_block_statement()
        elif token.type == TokenType.Identifier:
            node = self.parse_assignment_statement()
        else:
            node = None
        return node
    
    def get_statements(self):
        node = self.parse_statement()
        statements = [node]
        print(self.current_token)
        # find all lines in block
        while self.current_token.type == TokenType.Semicolon:
            self.eat(TokenType.Semicolon)
            # parse statement and skip to next semicolon
            statements.append(self.parse_statement())
        if self.current_token.type == TokenType.Identifier:
            self.error('missing semicolon')
        return statements
        
    def parse_block_statement(self):
        self.eat(TokenType.LBrace)
        statements = self.get_statements()
        self.eat(TokenType.RBrace)
        
        block = NodeBlock()
        block.children = statements
    
        return block
    
    def parse_factor(self):
        # handles value or (x ± x)
        token = self.current_token
        
        if token.type in (TokenType.Plus, TokenType.Minus):
            self.eat(token.type)
            node = NodeUnaryOp(token, self.parse_factor())
            return node
            
        elif token.type == TokenType.Number:
            self.eat(TokenType.Number)
            return NodeNumber(token)
        
        elif token.type == TokenType.LParen:
            self.eat(TokenType.LParen)
            node = self.parse_expression()
            print("***{0}".format(self.current_token))
            self.eat(TokenType.RParen)
            return node
        else:
            node = self.parse_variable()
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
        return self.parse_block_statement()

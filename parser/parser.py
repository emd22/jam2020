from lexer import LexerToken, TokenType, Keywords
from parser.node import *

# peter parser
    
class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_index = 0
        self.current_token = self.next_token()
    
    def next_token(self):
        if self.token_index+1 > len(self.lexer.tokens):
            return None
        #raise Exception('Token index out of range')
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
        varname = self.parse_variable()
        self.eat(TokenType.Equals)
        value = self.parse_expression()
        node = NodeAssign(varname, value)
        return node
    
    def parse_statement(self):
        token = self.current_token
        if token.type == TokenType.LBrace:
            # Start of new block
            node = self.parse_block_statement()
        elif token.type == TokenType.Identifier:
            # When identifier, parse assignment
            node = self.parse_assignment_statement()
        elif token.type == TokenType.Keyword:
            # Check if Let keyword
            if Keywords(token.value) == Keywords.Let:
                node = self.parse_variable_declaration()
        else:
            raise Exception('Unknown token {} in statement'.format(token.type))
            node = None
        if self.current_token.type != TokenType.Semicolon:
            raise Exception('Missing semicolon')
        return node
    
    def get_statements(self):
        node = self.parse_statement()
        statements = [node]
        # find all lines in block
        while self.current_token.type == TokenType.Semicolon:
            self.eat(TokenType.Semicolon)
            # We hit last statement in block, break
            if self.current_token.type == TokenType.RBrace:
                break
            # parse statement and skip to next semicolon
            statements.append(self.parse_statement())
        return statements
        
    def parse_block_statement(self):
        self.eat(TokenType.LBrace)
        statements = self.get_statements()
        self.eat(TokenType.RBrace)
        
        block = NodeBlock()
        block.children = statements
    
        return block
    
    def parse_type(self):
        node = NodeVarType(self.current_token)
        self.eat(self.current_token.type)
        return node
        
    def parse_variable_declaration(self):
        # let:TYPE parse_assignment_statement
        
        # eat let keyword
        self.eat(TokenType.Keyword)
        # manual type set
        vtype = None
        if self.current_token.type == TokenType.Colon:
            self.eat(TokenType.Colon)
            vtype = self.parse_type()
            
        vname = self.current_token
        val_node = self.parse_assignment_statement()
        
        # TODO: multiple variable declaration(e.g let:int var0,var1)
        vnodes = NodeDeclare(vtype, vname, val_node)
        
        return vnodes
    
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

from lexer import LexerToken, TokenType, Keywords
from error import errors, Error, ErrorType
from parser.node import *

# peter parser

class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
        self.token_index = 0
        self.current_token = self.next_token()
        
        self.keyword_methods = {
            'let': self.parse_variable_declaration,
            'if': self.parse_if_statement
        }
    
    def next_token(self):
        if self.token_index+1 > len(self.lexer.tokens):
            return None
            
        self.current_token = self.lexer.tokens[self.token_index]
        self.token_index += 1
        return self.current_token
    
    def peek_token(self, offset=0, token_type=None):
        # TODO: fix this garbage fire
        offset -= 1
        if self.token_index+offset > len(self.lexer.tokens):
            return None
        token = self.lexer.tokens[self.token_index+offset]
        
        if token_type is not None and token.type != token_type:
            return None
        
        return token
    
    def peek_keyword_token(self, keyword):
        token = self.peek_token(0, TokenType.Keyword)
            
        if token is not None and Keywords(token.value) == keyword:
            return keyword

        return None
    
    def error(self, message):
        # TODO: filename instead of none
        errors.push_error(Error(ErrorType.Syntax, self.current_token.location, message, "none"))
    
    def expect_token(self, token_type, offset=0):
        token = self.peek_token(offset)

        if token.type == token_type:
            return token
        else:
            self.error('Expected {0} but recieved {1}'.format(token_type, token.type))
            return None

    def eat(self, token_type=None):
        if token_type is not None:
            token = self.expect_token(token_type)

        self.current_token = self.next_token()

        return self.current_token
    
    def parse_variable(self):
        # create variable node and eat identifier
        node = NodeVariable(self.current_token)
        self.eat(TokenType.Identifier)
        return node
    
    def parse_assignment_statement(self, varname=None):
        if varname == None:
            varname = self.parse_variable()
            
        self.eat(TokenType.Equals)
    
        if self.current_token.type == TokenType.LParen:
            value = self.parse_parentheses()
        elif self.current_token.type == TokenType.LBrace:
            value = self.parse_block_statement()
        else:
            value = self.parse_expression()
        node = NodeAssign(varname, value)
        return node
    
    def parse_parentheses(self):
        # eat paren
        self.eat(TokenType.LParen)

        argument_list = None

        if self.peek_token(0) in (TokenType.RParen, TokenType.Identifier):
            expr = self.parse_expression()
            self.expect_token(TokenType.RParen)
            return expr

        elif self.peek_token(0, TokenType.RParen):
            # eat right paren
            self.eat(TokenType.RParen)

            argument_list = NodeArgumentList([])
        else:
            arguments = []

            while True:
                if self.expect_token(TokenType.Identifier) is None:
                    self.error('invalid argument format')
                    break

                # does not require let keyword
                argument = self.parse_variable_declaration(False)

                if argument is None:
                    self.error('invalid argument')
                    break

                arguments.append(argument)

                if self.peek_token(0, TokenType.Comma):
                    # eat comma and continue on with argument list
                    self.eat(TokenType.Comma)
                else:
                    break
            self.eat(TokenType.RParen)
            argument_list = NodeArgumentList(arguments)
        
        if argument_list is None:
            self.error('invalid argument list')
        else:
            return self.parse_function_expression(argument_list)

    def parse_statement(self):
        token = self.current_token
        if token.type == TokenType.LBrace:
            # Start of new block
            node = self.parse_block_statement()
            return node
        elif token.type == TokenType.Identifier:
            # parse function call
            if self.peek_token(1).type == TokenType.LParen:
                node = self.parse_function_call()
            # parse assignment
            else:
                node = self.parse_assignment_statement()
        elif token.type == TokenType.Keyword:
            node = self.parse_keyword()
        else:
            self.error('Unknown token {} in statement'.format(token.type))
            node = None
        
        if self.current_token.type != TokenType.Semicolon:
            self.error('Missing semicolon')
        return node
    
    def get_statements(self):
        if self.current_token.type == TokenType.RBrace:
            return []

        statements = [self.parse_statement()]
        
        # find all lines in block
        while self.current_token is not None and self.current_token.type == TokenType.Semicolon:
            self.eat(TokenType.Semicolon)
            # We hit last statement in block, break
            if self.current_token is None or self.current_token.type == TokenType.RBrace:
                break
            # parse statement and skip to next semicolon
            statements.append(self.parse_statement())

        return statements

    def parse_keyword(self):
        keyword = self.expect_token(TokenType.Keyword)
        #self.eat()

        method = None
        
        if keyword is not None:
            method = self.keyword_methods[keyword.value]

        if method is None:
            self.error('{0} is not a valid keyword'.format(keyword))

        return method()

    def parse_block_statement(self):
        self.eat(TokenType.LBrace)
        block = NodeBlock(self.current_token)
        block.children = self.get_statements()
        self.eat(TokenType.RBrace)

        return block
    
    def parse_type(self):
        node = NodeVarType(self.current_token)
        self.eat(self.current_token.type)
        return node
        
    def parse_function_call(self):
        # VAR (PARAM,...)
        
        var = NodeVariable(self.current_token)
        self.eat(TokenType.Identifier)
        self.eat(TokenType.LParen)
        
        # TODO: parameters
        
        self.eat(TokenType.RParen)
        node = NodeCall(var, None)
        return node

    def parse_function_expression(self, argument_list=None):
        if argument_list is None:
            argument_list = self.parse_parentheses()

        block = self.parse_block_statement()

        return NodeFunctionExpression(argument_list, block)
    
    def parse_variable_declaration(self, require_keyword=True):
        # let:TYPE parse_assignment_statement
        
        if require_keyword:
            # eat let keyword
            self.eat(TokenType.Keyword)
            
        vname = self.current_token
        self.eat(TokenType.Identifier)
        # manual type set
        vtype = None
        if self.current_token.type == TokenType.Colon:
            self.eat(TokenType.Colon)
            vtype = self.parse_type()
            
        if self.peek_token().type == TokenType.Equals:
            val_node = self.parse_assignment_statement(vname)
        else:
            val_node = NodeNone(vname)
        # TODO: multiple variable declaration(e.g let:int var0,var1)
        vnodes = NodeDeclare(vtype, vname, val_node)
        
        return vnodes
        
    def parse_if_statement(self): 
        expr = self.parse_expression()
        block = self.parse_block_statement()
        else_block = None
        
        if self.peek_keyword_token(Keywords.Else):
            # eat else
            self.eat(TokenType.Keyword)
            else_block = self.parse_block_statement()
            
        
        return NodeIfStatement(expr, block, else_block)
    
    def parse_factor(self):
        # handles value or (x ± x)
        token = self.current_token
        
        # handle +, -
        if token.type in (TokenType.Plus, TokenType.Minus):
            self.eat(token.type)
            node = NodeUnaryOp(token, self.parse_factor())
            return node
        
        # handle '!'
        elif token.type == TokenType.Not:
            self.eat(TokenType.Not)
            # != statement
            if (self.current_token.type == TokenType.Equals):
                node = NodeBinOp()
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
        tree = NodeBlock(self.current_token)
        tree.children = self.get_statements()

        if len(errors.errors) > 0:
            errors.print_errors()
            quit()

        return tree

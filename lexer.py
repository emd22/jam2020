import enum

class TokenType(enum.Enum):
    LParen = '('
    RParen = ')'
    LBrace = '{'
    RBrace = '}'
    Plus = '+'
    Minus = '-'
    Multiply = '*'
    Divide = '/'
    
    Identifier = 9
    Number = 10
    String = 11

    def get_type(self, value):
        if value == '':
            return None
                
        if (value in self._value2member_map_):
            return TokenType(value)
        if (value.isdigit()):
            return TokenType.Number

        elif (value[0] == '"' and value[-1] == '"'):
            return TokenType.String
        return TokenType.Identifier
    def has_value(self, value):
        # check if value exists in enum... wtf
        return value in self._value2member_map_

class LexerToken():
    def __init__(self, value):
        self.type = TokenType.get_type(TokenType, value)
        self.value = value
    def __str__(self):
        return "LexerToken[Type:{0}, Value:'{1}']".format(self.type, self.value)
    def __repr__(self):
        return self.__str__()

class Lexer():
    def __init__(self, data):
        self.tokens = []
        self.data = data
        self.token_data = ""
        self.index = 0
        
        self.in_string = False
        
    def read_char(self):
        if self.index+1 > len(self.data):
            return ''
        rval = self.data[self.index]
        self.index += 1
        return rval
    
    def peek_char(self, offset=1):
        idx = self.index+offset
        if idx >= len(self.data) or idx < 0:
            return ''
        return self.data[idx]
        
    def push_token(self):
        self.tokens.append(LexerToken(self.token_data))
        self.token_data = ""
    
    def skip_whitespace(self):
        if self.peek_char(0).isspace():
            while self.peek_char(0).isspace():
                self.read_char()
            return True
            #self.push_token()
        return False
    
    def lex(self):
        splitables = "();:+-*/"
        while self.peek_char(0) != '':
            if self.skip_whitespace() and not self.in_string:
                self.push_token()
                pass
            elif self.peek_char(0) in splitables and not self.in_string:
                if not self.peek_char(-1).isspace() and self.peek_char(-1) not in splitables:
                    self.push_token()
                self.token_data = self.read_char()
                self.push_token()
                self.skip_whitespace()
            else:
                # check if string character, toggle is_string
                if (self.peek_char(0) == '"'):
                    self.in_string = not self.in_string
                self.token_data += self.read_char()
        # still some data left in token_data, push to end
        if self.token_data != '':
            self.push_token()

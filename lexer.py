from enum import Enum, auto

class Keywords(Enum):
    Let = 'let'
    If = 'if'
    Else = 'else'
    Func = 'func'

class TokenType(Enum):
    LParen = '('
    RParen = ')'
    LBrace = '{'
    RBrace = '}'
    Plus = '+'
    Minus = '-'
    Multiply = '*'
    Divide = '/'
    Equals = '='
    Semicolon = ';'
    Colon = ':'
    Dot = '.'
    Comma = ','
    Not = '!'
    LessThan = '<'
    GreaterThan = '>'
    
    BitwiseOr = '|'
    BitwiseAnd = '&'
    BitwiseNot = '~'
    
    BitwiseLShift = auto()
    BitwiseRShift = auto()
    
    Identifier = auto()
    Number = auto()
    String = auto()
    Keyword = auto()

    def get_type(self, value):
        if value == '':
            return None
            
        if (value in self._value2member_map_):
            return TokenType(value)
            
        # TODO: add octal, hexadecimal and decimal numbers
        if value[0].isdigit():
            if len(value) > 1:
                if value[1] == 'x' or value[1] == 'X':
                    return TokenType.Number
            return TokenType.Number
        
        # TODO: add single quote strings
        elif value[0] == '"' and value[-1] == '"':
            return TokenType.String
        
        # check if string is keyword
        if value in Keywords._value2member_map_:
            return TokenType.Keyword
        
        # nothing else, must be identifier
        return TokenType.Identifier
        
    def has_value(self, value):
        # check if value exists in enum... wtf
        return value in self._value2member_map_

class LexerToken():
    def __init__(self, value):
        self.type = TokenType.get_type(TokenType, value)
        self.value = value
        self.location = (0, 0)
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
        
        # Error handling
        self.row = 1
        self.col = 1
        
        self.in_string = False
    
    # return character and progress through buffer
    def read_char(self, amt=1):
        if self.index+amt > len(self.data):
            return ''
        rval = self.data[self.index]
        self.index += amt
        self.col += 1
        if rval == '\n':
            self.col = 1
            self.row += 1
        return rval
    
    # return character and keep index
    def peek_char(self, offset=1):
        idx = self.index+offset
        if idx >= len(self.data) or idx < 0:
            return ''
        return self.data[idx]
    
    def push_token(self):
        token = LexerToken(self.token_data)
        token.location = (self.col, self.row)
        self.tokens.append(token)
        self.token_data = ""
    
    def skip_whitespace(self):
        if self.peek_char(0).isspace():
            while self.peek_char(0).isspace():
                self.read_char()
            return True
        return False
    
    def lex(self):
        splitables = "(){};:+-*/=.,!|&~<>^"
        self.skip_whitespace()
        while self.peek_char(0) != '':
            # encountered whitespace and not in string, push token
            if self.peek_char(0) == '/' and self.peek_char(1) == '*':
                # skip '/*' characters
                self.read_char(2)
                # read until '*/'
                while (self.read_char() != '*' and self.peek_char(1) != '/'):
                    pass
                # skip '*/' characters
                self.read_char(2)
                # skip any whitespace after comment
                self.skip_whitespace()
                continue
            
            elif not self.in_string and self.skip_whitespace():
                self.push_token()
                continue
                  
            elif self.peek_char(0) in splitables and not self.in_string:
                if not self.peek_char(-1).isspace() and self.peek_char(-1) not in splitables:
                    self.push_token()
                self.token_data = self.read_char()
                self.push_token()
                self.skip_whitespace()
                continue
  
            # check if string character, toggle is_string
            if (self.peek_char(0) == '"'):
                self.in_string = not self.in_string
            self.token_data += self.read_char()
        # still some data left in token_data, push to end
        if self.token_data != '':
            self.push_token()

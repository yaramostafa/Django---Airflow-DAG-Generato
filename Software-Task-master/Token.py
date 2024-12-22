# Token types used in parsing and interpreting the equations
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN,  ATTR, REGEX, COMMA, STRING = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'ATTR', 'REGEX', 'COMMA', 'STRING'
)

class Token:
    """
    Represents a single token in the input.
    Each token has a type and a value.
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self): # Magic function
        return self.__str__()

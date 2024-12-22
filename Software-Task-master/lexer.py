from Token import *

class Lexer:
    """
    Responsible for breaking down the input string (equation) into tokens.
    """
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        """Moves to the next character in the input."""
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        """Skips over whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Handles numeric values."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def string(self):
        """Handles string literals for regex patterns."""
        result = ''
        self.advance()  # Skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # Skip the closing quote
        return result

    def get_next_token(self):
        """
        Identifies the next token in the input string.
        Returns a token object or raises an error if no valid token is found.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char.isalpha():
                word = ''
                while self.current_char is not None and self.current_char.isalnum():
                    word += self.current_char
                    self.advance()
                if word == 'Regex':
                    return Token(REGEX, word)
                elif word == 'ATTR':
                    return Token(ATTR, word)

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == '"':
                return Token(STRING, self.string())

            raise Exception('Invalid character (lexical analysis).')

        return None

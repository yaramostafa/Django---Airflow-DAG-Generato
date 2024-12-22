# Composite Design Pattern
class AST:
    """
    Base class for Abstract Syntax Tree nodes.
    Other specific node types will inherit from this class.
    """
    pass


class BinOp(AST):
    """
    Represents a binary operation (e.g., addition, subtraction).
    """
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    """
    Represents a numeric value in the AST.
    """
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Regex(AST):
    """
    Represents a regex operation in the AST.
    """
    def __init__(self, attr, pattern):
        self.attr = attr
        self.pattern = pattern
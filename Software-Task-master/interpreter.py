import re
from operations import AddOperation, SubOperation, MulOperation, DivOperation
from parser import *

# Visitor Design Pattern
class NodeVisitor:
    """
    Base visitor class for traversing and interpreting the AST nodes.
    The visit method dynamically dispatches the node to the appropriate visitor method based on the node type.
    If no specific visitor method is found, it calls the generic_visit method.
    """
    def visit(self, node):
        # Calls the appropriate visit method based on the node type
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # For unsupported node types
        raise Exception(f'No visit_{type(node).__name__} method')


class Interpreter(NodeVisitor):
    """
    Interpreter class for evaluating AST nodes, supporting arithmetic operations and regex matching.
    """
    def __init__(self, parser, attr_value):
        self.parser = parser
        self.attr_value = attr_value
        # maps operation types to corresponding operation classes
        self.operations = {
            'PLUS': AddOperation(),
            'MINUS': SubOperation(),
            'MUL': MulOperation(),
            'DIV': DivOperation()
        }

    def visit_BinOp(self, node):
        """
        Visits a binary operation node (e.g., addition, subtraction) and evaluates it.
        Applies the appropriate operation (PLUS, MINUS, MUL, DIV) on the left and right child nodes.
        """
        operation = self.operations.get(node.op.type)
        if operation:
            return operation.apply(self.visit(node.left), self.visit(node.right))
        else:
            raise ValueError(f"Unsupported operation: {node.op.type}")

    def visit_Num(self, node):
        """
        Visits a number node and returns its value.
        """
        return node.value

    def visit_Regex(self, node):
        """
        Visits a regex node and performs regex matching on the attribute value.
        Returns a boolean indicating if the pattern matches the attribute value.
        """
        pattern = node.pattern.value
        return str(bool(re.match(pattern, self.attr_value)))

    def interpret(self):
        """
        Starts the interpretation process by parsing the input equation and visiting the root node.
        Returns the final result of the AST evaluation.
        """
        tree = self.parser.parse()
        return self.visit(tree)


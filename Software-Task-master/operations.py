# Strategy Design Pattern
class Operation:
    """Base class for all operations."""
    def apply(self, left, right):
        raise NotImplementedError("Each operation must implement 'apply'.")


class AddOperation(Operation):
    def apply(self, left, right):
        return left + right


class SubOperation(Operation):
    def apply(self, left, right):
        return left - right


class MulOperation(Operation):
    def apply(self, left, right):
        return left * right


class DivOperation(Operation):
    def apply(self, left, right):
        return left / right

'''
Leaf node class represents a leaf node on the expression tree.
'''

from typed_parser.node import Node
from typed_parser.tokenclass import Token

class LeafNode(Node):

    @staticmethod
    def build(token):
        # Guard against missing token argument
        if token is None:
            raise ValueError("Leaf Nodes require a valid Token argument")

        return LeafNode(token)

    def __init__(self, token):
        self._token = token

    # Return the string representation of the stored token
    def __str__(self):
        return str(self._token)

    # This is a leaf node, so to_list returns just this node's token in a Collection
    def to_list(self):
        return [self._token]

    # Return None since leaf nodes do not have children
    def get_children(self):
        return None

    # Return True since leaf nodes always have stored values
    def is_fruitful(self):
        return True

    # Return True if this LeafNode carries a Token which represents an operator
    def is_operator(self):
        operators = ['+', '-', '*', '/']
        return str(self._token) in operators
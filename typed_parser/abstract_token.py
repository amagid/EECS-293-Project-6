'''
Abstract Token class extends and fully implements the Token base class.
'''
from typed_parser.tokenclass import Token
from typed_parser.terminal_symbol import TerminalSymbol

class AbstractToken(Token):

    # Init defines _type attribute
    def __init__(self):

        # Internal type storage
        self._type = None

    # Retrieve and return this Token's type
    # Intentionally not abstract method since it is the same for all subclasses
    def get_type(self):
        return self._type

    # Check whether this Token matches the supplied type, and return the result
    # Intentionally not abstract method since it is the same for all subclasses
    def matches(self, token_type):
        return token_type is self._type
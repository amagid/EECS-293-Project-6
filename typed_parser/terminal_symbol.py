'''
TerminalSymbol enum provides encoding for different types of Tokens
'''
from typed_parser.leaf_node import LeafNode
from typed_parser.parse_state import ParseState, FAILURE
from enum import Enum

# TerminalSymbol enum
class TerminalSymbol(Enum):
    VARIABLE = 1
    PLUS = 2
    MINUS = 3
    TIMES = 4
    DIVIDE = 5
    OPEN = 6
    CLOSE = 7

    # Parse the first Token in the list and return a ParseState, return FAILURE state if fails
    def parse(self, token_list):
        
        if token_list != [] and token_list[0].matches(self):
            state = ParseState.build(LeafNode.build(token_list[0]), token_list[1:])
        else:
            state = FAILURE

        return state

    # Getter for internal _type field
    def get_type(self):
        return self.value
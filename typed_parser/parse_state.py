import copy

class ParseState():


    # Build a new ParseState with the given 'node' and 'remainder' arguments
    @staticmethod
    def build(node, remainder):
        if node is None:
            raise ValueError('ParseStates need a \'node\' argument')
        elif remainder is None:
            raise ValueError('ParseStates need a \'remainder\' argument')
        
        return ParseState(node, copy.copy(remainder))

    # Init takes arguments for current processed tree and remaining Token list
    def __init__(self, node, remainder, success=True):
        self._success = success
        self._node = node
        self._remainder = remainder

    # Getter for self._success
    def success(self):
        return self._success

    # Getter for self._node
    def node(self):
        return self._node

    # Getter for self._remainder
    def remainder(self):
        return copy.copy(self._remainder)

    # Check whether there is no remainder. Returns True if remainder list is empty
    def has_no_remainder(self):
        return self._remainder is None or self._remainder == []


# Module-static FAILURE state
FAILURE = ParseState(None, None, False)
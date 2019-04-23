from typed_parser.parse_state import ParseState, FAILURE
from typed_parser.internal_node import InternalNode

class SymbolSequence():

    @staticmethod
    def build(production):
        if production is None:
            raise ValueError('SymbolSequences must have a \'production\' argument')

        return SymbolSequence(production)

    @staticmethod
    def build_symbols(*arg):
        return SymbolSequence(list(arg))

    def __init__(self, production):
        self._production = production

    def __str__(self):
        return str(self._production)

    def match(self, token_list):
        # Guard against None token_list
        if token_list is None:
            raise ValueError('SymbolSequence cannot match to None token_list')

        # Track remainder and children
        remainder = token_list
        builder = InternalNode.Builder()

        # Attempt to parse each Token in the list
        for prod_symbol in self._production:
            state = prod_symbol.parse(remainder)

            if state.success():
                builder.add_child(state.node())
                remainder = state.remainder()
            else:
                return FAILURE
        
        # Return a ParseState containing a new InternalNode for the root and the remainder
        b = builder.build()
        
        return ParseState.build(b, remainder)

# Module-static EPSILON sequence
EPSILON = SymbolSequence.build([])
from enum import Enum
from typed_parser.terminal_symbol import TerminalSymbol
from typed_parser.symbol_sequence import SymbolSequence, EPSILON
from typed_parser.parse_state import ParseState, FAILURE
from typed_parser.utils import _str_to_token_list

class NonTerminalSymbol(Enum):
    EXPRESSION = 1
    EXPRESSION_TAIL = 2
    TERM = 3
    TERM_TAIL = 4
    UNARY = 5
    FACTOR = 6
    PRODUCTIONS = {}

    @staticmethod
    def parse_string_input(expression_string):
        return NonTerminalSymbol.parse_input(_str_to_token_list(expression_string))

    # Attempt to parse token_list as an EXPRESSION. Return None if fails
    @staticmethod
    def parse_input(token_list):
        # Attempt to parse the token_list as an EXPRESSION
        state = NonTerminalSymbol.EXPRESSION.parse(token_list)
        
        # If the parse was successful and has no remainder (fully parsed), return the resulting node
        if state.success() and state.has_no_remainder():
            return state.node()

        # Else, the parse failed (or didn't fully complete), so return None
        return None

    # Parse the token_list as this NonTerminalSymbol
    def parse(self, token_list):
        # Guard against None token_list
        if token_list is None:
            raise ValueError('NonTerminalSymbol cannot parse None token_list')

        # Retrieve best SymbolSequence for this next token
        symbol_seq = self._get_next_production(token_list)

        # If no match found, return FAILURE state
        if symbol_seq is None:
            return FAILURE
        
        # Else, continue parsing using this SymbolSequence
        state = symbol_seq.match(token_list)

        # Return the resulting ParseState
        return state

    def _get_next_production(self, token_list):
        token_type = None
        if token_list != []:
            token_type = token_list[0].get_type()

        return PRODUCTIONS[self][token_type]


# Module-private SEQUENCES table, used for generating PRODUCTIONS table.
# By-Token maps in PRODUCTIONS table are generated from this dictionary.
_SEQUENCES = {
    NonTerminalSymbol.EXPRESSION: [
        SymbolSequence.build([
            NonTerminalSymbol.TERM,
            NonTerminalSymbol.EXPRESSION_TAIL
        ])
    ],
    NonTerminalSymbol.EXPRESSION_TAIL: [
        SymbolSequence.build([
            TerminalSymbol.PLUS,
            NonTerminalSymbol.TERM,
            NonTerminalSymbol.EXPRESSION_TAIL
        ]),
        SymbolSequence.build([
            TerminalSymbol.MINUS,
            NonTerminalSymbol.TERM,
            NonTerminalSymbol.EXPRESSION_TAIL
        ]),
        EPSILON
    ],
    NonTerminalSymbol.TERM: [
        SymbolSequence([
            NonTerminalSymbol.UNARY,
            NonTerminalSymbol.TERM_TAIL
        ])
    ],
    NonTerminalSymbol.TERM_TAIL: [
        SymbolSequence([
            TerminalSymbol.TIMES,
            NonTerminalSymbol.UNARY,
            NonTerminalSymbol.TERM_TAIL
        ]),
        SymbolSequence([
            TerminalSymbol.DIVIDE,
            NonTerminalSymbol.UNARY,
            NonTerminalSymbol.TERM_TAIL
        ]),
        EPSILON
    ],
    NonTerminalSymbol.UNARY: [
        SymbolSequence([
            TerminalSymbol.MINUS,
            NonTerminalSymbol.FACTOR
        ]),
        SymbolSequence([
            NonTerminalSymbol.FACTOR
        ])
    ],
    NonTerminalSymbol.FACTOR: [
        SymbolSequence([
            TerminalSymbol.OPEN,
            NonTerminalSymbol.EXPRESSION,
            TerminalSymbol.CLOSE
        ]),
        SymbolSequence([
            TerminalSymbol.VARIABLE
        ])
    ]
}


# Module-static PRODUCTIONS table, used for looking up correct SymbolSequence
# based on next Token type. Configured using values from _SEQUENCES above.
PRODUCTIONS = {
    NonTerminalSymbol.EXPRESSION: {
        TerminalSymbol.VARIABLE: _SEQUENCES[NonTerminalSymbol.EXPRESSION][0],
        TerminalSymbol.PLUS: None,
        TerminalSymbol.MINUS: _SEQUENCES[NonTerminalSymbol.EXPRESSION][0],
        TerminalSymbol.TIMES: None,
        TerminalSymbol.DIVIDE: None,
        TerminalSymbol.OPEN: _SEQUENCES[NonTerminalSymbol.EXPRESSION][0],
        TerminalSymbol.CLOSE: None,
        None: None
    },
    NonTerminalSymbol.EXPRESSION_TAIL: {
        TerminalSymbol.VARIABLE: _SEQUENCES[NonTerminalSymbol.EXPRESSION_TAIL][2],
        TerminalSymbol.PLUS: _SEQUENCES[NonTerminalSymbol.EXPRESSION_TAIL][0],
        TerminalSymbol.MINUS: _SEQUENCES[NonTerminalSymbol.EXPRESSION_TAIL][1],
        TerminalSymbol.TIMES: _SEQUENCES[NonTerminalSymbol.EXPRESSION_TAIL][2],
        TerminalSymbol.DIVIDE: _SEQUENCES[NonTerminalSymbol.EXPRESSION_TAIL][2],
        TerminalSymbol.OPEN: _SEQUENCES[NonTerminalSymbol.EXPRESSION_TAIL][2],
        TerminalSymbol.CLOSE: _SEQUENCES[NonTerminalSymbol.EXPRESSION_TAIL][2],
        None: _SEQUENCES[NonTerminalSymbol.EXPRESSION_TAIL][2]
    },
    NonTerminalSymbol.TERM: {
        TerminalSymbol.VARIABLE: _SEQUENCES[NonTerminalSymbol.TERM][0],
        TerminalSymbol.PLUS: None,
        TerminalSymbol.MINUS: _SEQUENCES[NonTerminalSymbol.TERM][0],
        TerminalSymbol.TIMES: None,
        TerminalSymbol.DIVIDE: None,
        TerminalSymbol.OPEN: _SEQUENCES[NonTerminalSymbol.TERM][0],
        TerminalSymbol.CLOSE: None,
        None: None
    },
    NonTerminalSymbol.TERM_TAIL: {
        TerminalSymbol.VARIABLE: _SEQUENCES[NonTerminalSymbol.TERM_TAIL][2],
        TerminalSymbol.PLUS: _SEQUENCES[NonTerminalSymbol.TERM_TAIL][2],
        TerminalSymbol.MINUS: _SEQUENCES[NonTerminalSymbol.TERM_TAIL][2],
        TerminalSymbol.TIMES: _SEQUENCES[NonTerminalSymbol.TERM_TAIL][0],
        TerminalSymbol.DIVIDE: _SEQUENCES[NonTerminalSymbol.TERM_TAIL][1],
        TerminalSymbol.OPEN: _SEQUENCES[NonTerminalSymbol.TERM_TAIL][2],
        TerminalSymbol.CLOSE: _SEQUENCES[NonTerminalSymbol.TERM_TAIL][2],
        None: _SEQUENCES[NonTerminalSymbol.TERM_TAIL][2]
    },
    NonTerminalSymbol.UNARY: {
        TerminalSymbol.VARIABLE: _SEQUENCES[NonTerminalSymbol.UNARY][1],
        TerminalSymbol.PLUS: None,
        TerminalSymbol.MINUS: _SEQUENCES[NonTerminalSymbol.UNARY][0],
        TerminalSymbol.TIMES: None,
        TerminalSymbol.DIVIDE: None,
        TerminalSymbol.OPEN: _SEQUENCES[NonTerminalSymbol.UNARY][1],
        TerminalSymbol.CLOSE: None,
        None: None
    },
    NonTerminalSymbol.FACTOR: {
        TerminalSymbol.VARIABLE: _SEQUENCES[NonTerminalSymbol.FACTOR][1],
        TerminalSymbol.PLUS: None,
        TerminalSymbol.MINUS: None,
        TerminalSymbol.TIMES: None,
        TerminalSymbol.DIVIDE: None,
        TerminalSymbol.OPEN: _SEQUENCES[NonTerminalSymbol.FACTOR][0],
        TerminalSymbol.CLOSE: None,
        None: None
    }
}
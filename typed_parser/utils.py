from typed_parser.terminal_symbol import TerminalSymbol
from typed_parser.connector import Connector
from typed_parser.variable import Variable

TERMINAL_SYMBOL_TRANSLATIONS = {
    '+': TerminalSymbol.PLUS,
    '-': TerminalSymbol.MINUS,
    '*': TerminalSymbol.TIMES,
    '/': TerminalSymbol.DIVIDE,
    '(': TerminalSymbol.OPEN,
    ')': TerminalSymbol.CLOSE
}

# Helper method to allow me to define tests more easily
# Takes a string expression representation and generates a token_list from it
def _str_to_token_list(expr):
    token_list = []
    for char in expr:
        if char in TERMINAL_SYMBOL_TRANSLATIONS:
            token_list.append(Connector.build(TERMINAL_SYMBOL_TRANSLATIONS[char]))
        else:
            token_list.append(Variable.build(char))
    return token_list
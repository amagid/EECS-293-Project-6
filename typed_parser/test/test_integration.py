import pytest
from typed_parser.type_parser import TypeParser
from typed_parser.non_terminal_symbol import NonTerminalSymbol

TYPE_RULES = [
    [['int', '+', 'int'], 'int']
]

VARIABLE_TYPES = [
    [['a'], 'int'],
    [['b'], 'int']
]

def test_integration():
    type_parser = TypeParser()
    type_parser.import_types(TYPE_RULES, VARIABLE_TYPES)

    parse_tree = NonTerminalSymbol.parse_string_input('a+b')

    final_type = type_parser.expression_type(parse_tree)
    print(final_type)
    assert False
import pytest
from typed_parser.type_parser import TypeParser
from typed_parser.non_terminal_symbol import NonTerminalSymbol

TYPE_RULES = [
    [['int', '+', 'int'], 'int'],
    [['int', '+', 'double'], 'double'],
    [['double', '+', 'int'], 'double'],
    [['string', '+', '?'], 'string'],
    [['int', '-', 'int'], 'int'],
    [['double', '-', 'double'], 'double'],
    [['double', '-', 'int'], 'double'],
    [['int', '-', 'double'], 'double'],
    [['int', '*', 'int'], 'int'],
    [['double', '*', 'int'], 'double'],
    [['int', '*', 'double'], 'double'],
    [['double', '*', 'double'], 'double'],
    [['string', '*', 'int'], 'string'],
    [['int', '/', 'int'], 'int'],
    [['int', '/', 'double'], 'double'],
    [['int', 'weewoo', 'int'], 'string'],
    [['myfunction', '+', 'int'], 'brettjohnson'],
    [['-', '?'], '?']
]

VARIABLE_TYPES = [
    [['a'], 'int'],
    [['b'], 'double'],
    [['c'], 'string'],
    [['d'], 'int'],
    [['m'], 'myfunction']
]

BASIC_RULE_TEST_CASES = [
    ('a+d', 'int'),
    ('a+b', 'double'),
    ('c+m', 'string'),
    ('c+a', 'string'),
    ('m+a', 'brettjohnson'),
    ('d/a', 'int'),
    ('c*a', 'string'),
    ('a+-d', 'int'),
    ('a/c', None),
    ('m+(a*d+a-d)', 'brettjohnson'),
    ('a+a+a+a+a+a+a+d+a+d+a+d+a+d+a+a+a+a+a+a+a+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d+d', 'int')
]

@pytest.mark.parametrize(
    'test_case', BASIC_RULE_TEST_CASES
)
def test_integration(test_case):
    type_parser = TypeParser()
    type_parser.import_types(TYPE_RULES, VARIABLE_TYPES)

    parse_tree = NonTerminalSymbol.parse_string_input(test_case[0])

    final_type = type_parser.expression_type(parse_tree)

    assert final_type == test_case[1]
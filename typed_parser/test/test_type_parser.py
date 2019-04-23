import pytest
from typed_parser.type_parser import TypeParser
from typed_parser.non_terminal_symbol import NonTerminalSymbol
from typed_parser.variable import Variable
from typed_parser.connector import Connector

def _basic_type_parser():
    type_rules = [
        [['int', '+', 'int'], 'double'],
        [['-', 'int'], 'string'],
    ]
    variable_types = [
        [['a'], 'int']
    ]
    type_parser = TypeParser()
    type_parser.import_types(type_rules, variable_types)

    return type_parser, type_rules, variable_types


def test_init():
    type_parser = TypeParser()
    assert type_parser is not None

def test_import_types_sorts_rules_by_length():
    type_parser, _, variable_types = _basic_type_parser()

    assert type_parser._type_rules[1][0]._input_types == variable_types[0][0]
    assert type_parser._type_rules[1][0]._output_type == variable_types[0][1]

def test_expression_type_no_node():
    type_parser, _, _ = _basic_type_parser()

    assert type_parser.expression_type(None) is None

def test_expresstion_type_childless_node():
    type_parser, _, variable_types = _basic_type_parser()

    assert type_parser.expression_type(NonTerminalSymbol.parse_string_input('a')) == variable_types[0][1]

def test_has_unary_negation():
    type_parser, _, _ = _basic_type_parser()

    assert type_parser._has_unary_negation(['-'], [])

def test_has_no_unary_negation():
    type_parser, _, _ = _basic_type_parser()

    assert not type_parser._has_unary_negation(['+'], [1,2,3,4])
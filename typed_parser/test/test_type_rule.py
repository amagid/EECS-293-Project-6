import pytest
from typed_parser.type_rule import TypeRule

def test_init_simple_input():
    input_types = ['int', '+', 'int']
    output_type = 'int'
    type_rule = TypeRule(input_types, output_type)

    assert type_rule._input_types == input_types
    assert type_rule._output_type == output_type

def test_init_2_input_unary_negation_allowed():
    input_types = ['-', 'int']
    output_type = 'int'
    type_rule = TypeRule(input_types, output_type)

    assert type_rule._input_types == input_types
    assert type_rule._output_type == output_type

def test_init_2_input_not_unary_negation_not_allowed():
    input_types = ['+', 'int']
    output_type = 'int'

    with pytest.raises(AssertionError):
        type_rule = TypeRule(input_types, output_type)

def test_init_wildcard():
    input_types = ['?']
    output_type = 'int'
    type_rule = TypeRule(input_types, output_type)

    assert type_rule._input_types == input_types
    assert type_rule._output_type == output_type
    assert type_rule._wildcard_index == 0

def test_apply_normal_match():
    input_types = ['int', '+', 'int']
    output_type = 'int'
    type_rule = TypeRule(input_types, output_type)
    expression = ['int', '+', 'int']

    assert type_rule.apply(expression) == output_type

def test_apply_no_match():
    input_types = ['int', '-', 'int']
    output_type = 'int'
    type_rule = TypeRule(input_types, output_type)
    expression = ['int', '+', 'int']

    assert type_rule.apply(expression) is None

def test_apply_wildcard_match():
    input_types = ['int', '+', '?']
    output_type = 'int'
    type_rule = TypeRule(input_types, output_type)
    expression = ['int', '+', 'string']

    assert type_rule.apply(expression) == output_type

def test_wildcard_matches_no_different_lengths():
    type_rule = TypeRule(['?'], '?')
    result = type_rule._wildcard_matches(['int', '+', 'int'])

    assert not result

def test_wildcard_matches_with_wildcard():
    type_rule = TypeRule(['int', '+', '?'], 'int')

    assert type_rule._wildcard_matches(['int', '+', 'int'])

def test_wildcard_matches_with_wildcard_bad_structure():
    type_rule = TypeRule(['int', '-', '?'], 'int')

    assert not type_rule._wildcard_matches(['int', '+', 'int'])

def test_apply_wildcard_wildcard_output():
    type_rule = TypeRule(['int', '+', '?'], '?')
    result = type_rule._apply_wildcard('string')

    assert result == 'string'

def test_apply_wildcard_constant_output():
    type_rule = TypeRule(['int', '+', '?'], 'int')
    result = type_rule._apply_wildcard('string')

    assert result == 'int'
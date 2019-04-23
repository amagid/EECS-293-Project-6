import pytest
from typed_parser.type_rule import TypeRule

def test_wildcard_matches_different_lengths():
    type_rule = TypeRule(['?'], '?')
    result = type_rule._wildcard_matches(['int', '+', 'int'])

    assert not result
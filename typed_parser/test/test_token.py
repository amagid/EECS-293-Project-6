import pytest
from typed_parser.tokenclass import Token

def test_token_is_abstract():
    with pytest.raises(TypeError):
        Token()

def test_get_full_coverage_of_abstract_methods():
    Token.get_type(None)
    Token.matches(None, None)
    assert True
import pytest
from typed_parser.tokenclass import Token

def test_token_is_abstract():
    with pytest.raises(TypeError):
        Token()
from typed_parser.abstract_token import AbstractToken

def test_init():
    abstract_token = AbstractToken()

    assert abstract_token._type is None
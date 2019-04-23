import pytest
from typed_parser.variable import Variable
from typed_parser.terminal_symbol import TerminalSymbol

def test_error_on_no_representation():
    with pytest.raises(ValueError):
        Variable(None)

def test_variable_caching():
    var = Variable.build('x')
    assert Variable.build('x') is var

def test_variable_type_matches():
    assert Variable.build('x').matches(TerminalSymbol.VARIABLE)

def test_variable_str():
    assert str(Variable.build('x')) == 'x'

def test_variable_representation():
    assert Variable.build('x').representation() == 'x'

def test_variable_not_equal():
    assert Variable.build('x') != Variable.build('y')
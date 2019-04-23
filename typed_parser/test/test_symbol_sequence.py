import pytest
from typed_parser.symbol_sequence import SymbolSequence, EPSILON
from typed_parser.connector import Connector
from typed_parser.variable import Variable
from typed_parser.terminal_symbol import TerminalSymbol
from typed_parser.parse_state import ParseState, FAILURE

# Helper method to generate a SymbolSequence for '(a+b)'
def _generate_test_symbol_sequence():
    terminal_symbols = [
        TerminalSymbol.OPEN,
        TerminalSymbol.VARIABLE,
        TerminalSymbol.PLUS,
        TerminalSymbol.VARIABLE,
        TerminalSymbol.CLOSE
    ]
    production = _generate_production_from_terminal_symbols(terminal_symbols)
    
    return terminal_symbols, production, SymbolSequence.build(terminal_symbols)

# Helper method to generate a SymbolSequence with an empty production
def _generate_empty_symbol_sequence():
    return [], [], EPSILON

# Helper method to generate a SymbolSequence with one Token in it
def _generate_1_token_symbol_sequence():
    terminal_symbols = [TerminalSymbol.OPEN]
    production = _generate_production_from_terminal_symbols(terminal_symbols)
    return terminal_symbols, production, SymbolSequence.build(terminal_symbols)

# Helper method to generate a list of built Tokens from a list of TerminalSymbols
def _generate_production_from_terminal_symbols(terminal_symbols):
    # List of variable names to generate test variables from
    variable_names = ['d', 'c', 'b', 'a']

    # Build Token from each supplied TerminalSymbol & add to production
    production = []
    for ts in terminal_symbols:
        if ts is not TerminalSymbol.VARIABLE:
            production.append(Connector.build(ts))
        else:
            production.append(Variable.build(variable_names.pop()))

    return production

# Test that EPSILON is created
def test_epsilon_is_correct_type():
    epsilon = EPSILON
    assert type(epsilon) is SymbolSequence

# Test that EPSILON has empty production
def test_epsilon_has_correct_attributes():
    epsilon = EPSILON
    assert type(epsilon._production) is list
    assert epsilon._production == []

# Ensure that build() gives ValueError when production is None
def test_build_error_on_none_production():
    with pytest.raises(ValueError):
        SymbolSequence.build(None)

# Ensure that str(SymbolSequence) returns the same as str(SymbolSequence._production)
def test_str_delegates_to_production():
    terminal_symbols, _, seq = _generate_test_symbol_sequence()
    assert str(seq) == str(terminal_symbols)

# Ensure that the build_symbols() method assigns the production the same as build()
def test_build_symbols_assigns_production():
    terminal_symbols, _, seq = _generate_test_symbol_sequence()
    seq2 = SymbolSequence.build_symbols(terminal_symbols[0], terminal_symbols[1], terminal_symbols[2], terminal_symbols[3], terminal_symbols[4])

    assert seq._production == seq2._production

# Match should raise ValueError when token_list is None
def test_match_error_on_none_token_list():
    _, _, seq = _generate_test_symbol_sequence()

    with pytest.raises(ValueError):
        seq.match(None)

# Match should return a ParseState
def test_match_returns_parse_state():
    state = EPSILON.match([])

    assert type(state) is ParseState

# Test match empty seq with empty prod
def test_match_empty_seq_empty_prod():
    state = EPSILON.match([])

    assert state.success()
    assert state.remainder() == []

# Test match empty seq with 1 token prod
def test_match_empty_seq_1_token_prod():
    _, prod, _ = _generate_1_token_symbol_sequence()
    state = EPSILON.match(prod)

    assert state.success()
    assert state.remainder() == prod

# Test match empty seq with large prod
def test_match_empty_seq_large_prod():
    _, prod, _ = _generate_test_symbol_sequence()
    state = EPSILON.match(prod)

    assert state.success()
    assert state.remainder() == prod

# Test match 1 token seq with empty prod
def test_match_1_token_seq_empty_prod_fails():
    _, _, seq = _generate_1_token_symbol_sequence()
    _, prod, _ = _generate_empty_symbol_sequence()
    state = seq.match(prod)

    assert state is FAILURE

# Test match 1 token seq with 1 token prod which matches
def test_match_1_token_seq_1_token_prod_matches():
    # Duplicate calls to construct a different prod reference than was used to make seq
    _, _, seq = _generate_1_token_symbol_sequence()
    _, prod, _ = _generate_1_token_symbol_sequence()
    state = seq.match(prod)

    assert state.success()
    assert state.remainder() == []

# Test match 1 token seq with 1 token prod which does not match
def test_match_1_token_seq__1_token_prod_fails():
    _, _, seq = _generate_1_token_symbol_sequence()
    prod = [Connector.build(TerminalSymbol.MINUS)]
    state = seq.match(prod)

    assert state is FAILURE

# Test match 1 token seq with large prod which matches
def test_match_1_token_seq_large_prod_matches():
    seq = SymbolSequence.build([TerminalSymbol.OPEN])
    _, prod, _ = _generate_test_symbol_sequence()
    state = seq.match(prod)

    assert state.success()
    assert state.remainder() == prod[1:]

# Test match 1 token seq with large prod which does not match
def test_match_1_token_seq_large_prod_fails():
    seq = SymbolSequence.build([TerminalSymbol.CLOSE])
    _, prod, _ = _generate_test_symbol_sequence()
    state = seq.match(prod)

    assert state is FAILURE

# Test match large seq with empty prod
def test_match_large_seq_empty_prod_fails():
    _, _, seq = _generate_test_symbol_sequence()
    prod = []
    state = seq.match(prod)

    assert state is FAILURE

# Test match large seq with 1 token prod
def test_match_large_seq_1_token_prod_fails():
    _, _, seq = _generate_test_symbol_sequence()
    _, prod, _ = _generate_1_token_symbol_sequence()
    state = seq.match(prod)

    assert state is FAILURE

# Test match large seq with large prod which matches
def test_match_large_seq_large_prod_matches():
    # Duplicate calls to construct a different prod reference than was used to make seq
    _, _, seq = _generate_test_symbol_sequence()
    _, prod, _ = _generate_test_symbol_sequence()
    state = seq.match(prod)

    assert state.success()
    assert state.remainder() == []

# Test match large seq with large prod which does not match
def test_match_large_seq_large_prod_fails():
    _, _, seq = _generate_test_symbol_sequence()
    _, prod, _ = _generate_test_symbol_sequence()
    prod.insert(0, Variable.build('e'))
    state = seq.match(prod)

    assert state is FAILURE
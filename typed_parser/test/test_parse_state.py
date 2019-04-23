import pytest
from typed_parser.parse_state import ParseState, FAILURE

# Helper method to generate a ParseState
def _generate_test_parse_state():
    remainder = [1, 2, [3, 4, [5], 6], 7]
    node = True
    state = ParseState(node, remainder)
    return remainder, node, state

# Make sure FAILURE state is generated correctly
def test_failure_state_is_correct_type():
    failure_state = FAILURE
    assert type(failure_state) is ParseState

# Make sure the attributes of FAILURE state are correct to specs
def test_failure_state_has_correct_attributes():
    assert not FAILURE.success()
    assert FAILURE.node() is None
    assert FAILURE.remainder() is None

# Test that build() raises ValueError when no node is supplied
def test_build_error_on_no_node():
    with pytest.raises(ValueError):
        ParseState.build(None, [])
        
# Test that build() raises ValueError when no remainder is supplied
def test_build_error_on_no_remainder():
    with pytest.raises(ValueError):
        ParseState.build(True, None)

# Test that build() defaults to _success = True when args are valid
def test_build_assigns_success_true():
    _, _, state = _generate_test_parse_state()

    assert state.success()

# Test that build() actually used the args we gave
def test_build_assigns_given_fields():
    remainder, node, state = _generate_test_parse_state()

    assert state.node() is node
    assert state.remainder() == remainder

# Test that the remainder is deep-copied properly
def test_build_deep_copy_remainder():
    remainder, _, state = _generate_test_parse_state()

    assert remainder == state.remainder()
    assert remainder is not state.remainder()

# Test that has_no_remainder() returns True when _remainder is []
def test_has_no_remainder_list_empty():
    _, _, state = _generate_test_parse_state()
    state._remainder = []

    assert state.has_no_remainder()

# Test that has_no_remainder() returns True when _remainder is None
def test_has_no_remainder_list_none():
    _, _, state = _generate_test_parse_state()
    state._remainder = None

    assert state.has_no_remainder()

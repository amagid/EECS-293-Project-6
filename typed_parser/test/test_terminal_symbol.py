import pytest
from typed_parser.terminal_symbol import TerminalSymbol
from typed_parser.parse_state import ParseState, FAILURE
from typed_parser.connector import Connector
from typed_parser.variable import Variable
from typed_parser.leaf_node import LeafNode

# Helper method to generate a sample Token list: '(x+y)'
def _generate_token_list():
    return [
        Connector.build(TerminalSymbol.OPEN),
        Variable.build('x'),
        Connector.build(TerminalSymbol.PLUS),
        Variable.build('y'),
        Connector.build(TerminalSymbol.CLOSE)
    ]

# Helper method to generate full test data including:
# A TerminalSymbol, Token List, and ParseState
def _generate_test_data():
    ts = TerminalSymbol.OPEN
    token_list = _generate_token_list()
    state = ts.parse(token_list)

    return ts, token_list, state

# Test that we get FAILURE when the first token doesn't match this TerminalSymbol
def test_failure_on_unmatched_token():
    ts_plus = TerminalSymbol.PLUS
    state = ts_plus.parse(_generate_token_list())

    assert state is FAILURE

# Test that ParseState._success is True when first token does match
def test_success_on_matched_token():
    _, _, state = _generate_test_data()

    assert state.success()

# Test that we get back a LeafNode, not an InternalNode
def test_node_is_leaf_node_on_matched_token():
    _, _, state = _generate_test_data()

    assert type(state.node()) is LeafNode

# Test that the node we get back contains the matched Token
def test_node_contains_token_on_matched_token():
    _, token_list, state = _generate_test_data()

    assert state.node().to_list() == [token_list[0]]

# Test that the remainder loses its first Token when parsed
def test_remainder_pops_first_token_on_matched_token():
    _, token_list, state = _generate_test_data()

    assert state.remainder()[0] == token_list[1]

# Test that the remainder still contains the rest of the token list after parsing first token
def test_remainder_contains_rest_of_token_list():
    _, token_list, state = _generate_test_data()

    assert state.remainder() == token_list[1:]
    
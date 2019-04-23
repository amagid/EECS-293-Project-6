import pytest
from typed_parser.leaf_node import LeafNode
from typed_parser.connector import Connector
from typed_parser.terminal_symbol import TerminalSymbol

def test_error_on_none_children():
    with pytest.raises(ValueError):
        LeafNode.build(None)

def test_build_returns_internal_node():
    node = LeafNode.build(Connector.build(TerminalSymbol.PLUS))
    assert type(node) == LeafNode

def test_error_on_no_token():
    with pytest.raises(ValueError):
        LeafNode.build(None)

def test_str_with_connector():
    ln = LeafNode.build(Connector.build(TerminalSymbol.PLUS))
    assert str(ln) == '+'

def test_to_list_with_connector():
    conn = Connector.build(TerminalSymbol.PLUS)
    ln = LeafNode.build(conn)
    assert ln.to_list() == [conn]
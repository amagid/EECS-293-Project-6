import pytest
from typed_parser.node import Node

def test_node_is_abstract():
    with pytest.raises(TypeError):
        Node()

def test_get_node_coverage_even_though_it_is_abstract():
    Node.to_list(None)
    Node.get_children(None)
    Node.is_fruitful(None)
    Node.is_operator(None)
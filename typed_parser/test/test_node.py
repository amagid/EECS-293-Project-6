import pytest
from typed_parser.node import Node

def test_node_is_abstract():
    with pytest.raises(TypeError):
        Node()
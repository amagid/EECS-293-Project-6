import pytest
from typed_parser.internal_node import InternalNode

# Quick mock node class to allow for testing

class MockNode():
    def __init__(self):
        pass
    
    def to_list(self):
        return []

    def __str__(self):
        return '[]'

# Tests

def test_error_on_none_children():
    with pytest.raises(ValueError):
        InternalNode.build(None)

def test_build_returns_internal_node():
    node = InternalNode.build([])
    assert type(node) == InternalNode

def test_empty_children_str():
    node = InternalNode.build([])
    assert str(node) == '[]'

def test_empty_children_list():
    node = InternalNode.build([])
    assert node.to_list() == []

def test_recurse_on_1_child_str():
    node = InternalNode.build([1])
    assert str(node) == '[1]'

def test_recurse_on_1_child_list():
    node = InternalNode.build([MockNode()])
    assert node.to_list() == [[]]

def test_recurse_on_many_child_str():
    node = InternalNode.build([1,2,3])
    assert str(node) == '[1,2,3]'

def test_recurse_on_many_child_list():
    node = InternalNode.build([MockNode(), MockNode(), MockNode()])
    assert node.to_list() == [[], [], []]


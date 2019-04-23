'''
Internal node class represents an internal node on the expression tree.
'''
import copy
from typed_parser.node import Node
from typed_parser.tokenclass import Token
from typed_parser.leaf_node import LeafNode

class InternalNode(Node):

    # Builder nested class
    class Builder():

        def __init__(self):
            self._children = []

        # Remove childless nodes and collapse single-child nodes
        def simplify(self):
            for i in range(0, len(self._children)):
                self._update_children(self._children, i, self._simplify_node(self._children[i]))

            self._children = self._collapse_none_children(self._children)

            return self

        # Recursive method which does the bulk of simplification work
        def _simplify_node(self, node, parent_is_operator=False):
            children = node.get_children()

            # If this node is a leaf node, return the node
            if children is None:
                return [node]

            # If this node has more than one child, recurse on children
            if len(children) > 1:
                for i in range(0, len(children)):
                    self._update_children(children, i, self._simplify_node(children[i], node.is_operator()))

                # Remove children from list if they are None
                children = self._collapse_none_children(children)
                node._children = children

            # Handle 0 children, 1 child, still >1 children, and newly leaf node cases, then return the node
            return self._post_process_node(node, parent_is_operator)

        # Remove the child at index and replace it with the contents of new_children
        def _update_children(self, children, index, new_children):
            children.pop(index)
            while new_children != []:
                children.insert(index, new_children.pop())

        # Simplification helper method which removes None elements from node _children list
        def _collapse_none_children(self, children):
            return list(filter(self._remove_nones, children))

        # Filter function to test if a child is None
        def _remove_nones(self, child):
            return child is not None

        # Simplification helper method which re-processes nodes after their children have been processed (changes may have occurred)
        def _post_process_node(self, node, parent_is_operator):
            children = node.get_children()

            # If this node has one child, replace this node with its child & recurse
            if len(children) == 1:
                return self._simplify_node(children[0], node.is_operator())
                
            # If this node has no children, delete it
            if children == []:
                return []

            if node.is_operator() and not parent_is_operator:
                return children

            # If this node still has more children or is a leaf, return it as-is
            return [node]

        # Simplify and convert to InternalNode
        def build(self):
            # Simplify Builder
            self.simplify()

            # If there is only one child, return that child
            if len(self._children) == 1:
                return self._children[0]

            # Else, return children wrapped in an InternalNode
            return InternalNode.build(self._children)

        # Add a child to this Builder
        def add_child(self, node):
            self._children.append(node)
            return True


    # Static method to build and return a new InternalNode with the given children
    @staticmethod
    def build(children):
        # Guard against None children argument
        if children is None:
            raise ValueError('InternalNodes must receive an array of children')

        return InternalNode(children)

    def __init__(self, children):
        self._children = children

    # Return the string representation of the stored token
    def __str__(self):
        return '[' + ','.join(str(child) for child in self._children) + ']'

    # This is an internal node, so it returns the concatenation of its children's lists
    def to_list(self):
        output = []
        for child in self._children:
            output.append(child.to_list())

        return output

    # Return a copy of this node's children
    def get_children(self):
        return copy.copy(self._children)

    # Return True if this node has children
    def is_fruitful(self):
        return self._children is not None and self._children != []

    # Return True if this InternalNode's first child exists, is a LeafNode, and represents an operator
    def is_operator(self):
        return self.is_fruitful() and type(self._children[0]) is LeafNode and self._children[0].is_operator()

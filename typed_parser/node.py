'''
Node base class
'''

from abc import ABC, abstractmethod

class Node(ABC):

    # to_list method returns subtree under this node as a Collection
    @abstractmethod
    def to_list(self):
        pass

    # Returns a copy of the children of this node (None if leaf)
    @abstractmethod
    def get_children(self):
        pass

    # Returns True if node has children or is a leaf
    @abstractmethod
    def is_fruitful(self):
        pass

    # Returns True if the Node is a Leaf containing an operator
    # or if its first child is
    @abstractmethod
    def is_operator(self):
        pass

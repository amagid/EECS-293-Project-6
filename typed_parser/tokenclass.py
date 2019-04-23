'''
Main Token storage file, including general Token class.
'''

from abc import ABC, abstractmethod

class Token(ABC):

    # Retrieve and return this Token's type
    @abstractmethod
    def get_type(self):
        pass

    # Check whether this Token matches the supplied type, and return the result
    @abstractmethod
    def matches(self, token_type):
        pass
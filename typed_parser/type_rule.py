# Instances of the TypeRule class define how to determine the type of an expression structure. A TypeRule has an internally-stored list of string representations, as well as an internally-stored string type output. TypeRules are generic by design, but have a few restrictions on their input and output tokens:
# - There must be **exactly one** string output token - an expression must become a type, not another expression.
# - There must be **one, two, or three** string input tokens.
# - If there is only one string input token, it **must not** be equal to the string output token.
# - If there are two string input tokens, the first **must** be MINUS.

class TypeRule:
    def __init__(self, input_types, output_type):
        # Guard against any bad type rule inputs
        assert type(output_type) is str, "There must be only one output type, and it must be represented by a string"
        assert type(input_types) is list, "Input Types must be in a list"
        assert len(input_types) in range(1, 4), "The number of input types must be on [1,3]"
        if len(input_types) == 2:
            assert input_types[0] == '-', "Two-input rules must begin with '-' for unary negation"

        self._input_types = input_types
        self._output_type = output_type

    def apply(self, input_token_list):
        if input_token_list == self._input_types:
            return self._output_type
        else:
            return None
class TypeRule:
    """
    Instances of the TypeRule class define how to determine the type of an expression structure. A TypeRule has an internally-stored list of string representations, as well as an internally-stored string type output. TypeRules are generic by design, but have a few restrictions on their input and output tokens:
    - There must be **exactly one** string output token - an expression must become a type, not another expression.
    - There must be **one, two, or three** string input tokens.
    - If there is only one string input token, it **must not** be equal to the string output token.
    - If there are two string input tokens, the first **must** be MINUS.
    """

    def __init__(self, input_types, output_type):
        """
        Create a new TypeRule using the supplied input token array and output
        type.

        Params:

        - `list<string>` *input_types* - The pattern of types for this rule to match
        - `string` *output_type* - The type to output when this TypeRule matches an expression

        Returns:

        - `TypeRule`

        """

        # Guard against any bad type rule inputs
        assert type(output_type) is str, "There must be only one output type, and it must be represented by a string"
        assert type(input_types) is list, "Input Types must be in a list"
        assert len(input_types) in range(1, 4), "The number of input types must be on [1,3]"
        if len(input_types) == 2:
            assert input_types[0] == '-', "Two-input rules must begin with '-' for unary negation"

        self._input_types = input_types
        self._output_type = output_type

        # Check if this rule is a wildcard rule - for ease of use
        if '?' in input_types:
            self._wildcard_index = self._input_types.index('?')
        else:
            self._wildcard_index = None

    def apply(self, input_token_list):
        """
        Attempt to apply this TypeRule to the given set of input Type tokens.

        Params: 

        - `list<string>` *input_token_list*

        Returns:

        - `string` - The output type for this expression, if matched
        - `None` - if not matched

        """

        if input_token_list == self._input_types:
            return self._output_type
        # Apply deeper wildcard checking if this rule has a wildcard
        elif self._wildcard_index is not None and self._wildcard_matches(input_token_list):
            return self._apply_wildcard(input_token_list[self._wildcard_index])
        else:
            return None

    def _wildcard_matches(self, input_token_list):
        """
        Check if this wildcard-based TypeRule could be applied to the given input.
        While wildcard expressions can be catch-alls, they can also have some
        defined types in them to give them specific structure.

        Params:

        - `list<string>` *input_token_list*

        Returns:

        - `boolean`

        """

        if len(self._input_types) != len(input_token_list):
            return False

        for i in range(len(self._input_types)):
            if self._input_types[i] != input_token_list[i] and self._input_types[i] != '?':
                return False

        return True

    def _apply_wildcard(self, token):
        """
        Return the appropriate type for the given wildcard-matched token.
        If the output_type of this TypeRule is specified as a real type, it
        will output that type when the wildcard is matched. However, if the
        output type is specified as a wildcard ('?'), this method will return
        the type of the token *in the input that matched the wildcard*.

        Params:

        - `string` *token* - The specific input token that matched the wildcard

        Returns:
        - `string`
        
        """

        if self._output_type == '?':
            return token
        else:
            return self._output_type
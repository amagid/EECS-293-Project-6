# Instances of the TypeRule class define how to determine the type of an expression structure. A TypeRule has an internally-stored list of string representations, as well as an internally-stored string type output. TypeRules are generic by design, but have a few restrictions on their input and output tokens:
# - There must be **exactly one** string output token - an expression must become a type, not another expression.
# - There must be **one, two, or three** string input tokens.
# - If there is only one string input token, it **must not** be equal to the string output token.
# - If there are two string input tokens, the first **must** be MINUS and the second **must** be a type.
# - If there are three string input tokens, the first and third **must** be types and the middle **must** be a connector.

# The TypeRule class exposes a TypeRule.apply(Node) method which returns the type resulting from applying the given TypeRule on the expression rooted at Node, as well as the number of tokens that were matched. This method returns None if the TypeRule cannot be applied to this Node.

# class TypeRule:
    # INIT(input_types, output_type):
        # Store the input and output types internally, assert that they are all valid including in their organization

    # APPLY(input_token_list):
        # If the input_token_list matches this TypeRule's input token list, return this TypeRule's output type
        # Else, return None
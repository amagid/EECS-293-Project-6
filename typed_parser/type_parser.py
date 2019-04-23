# This is the entry point of the application. TypeParser provides a static entry method, determineExpressionType, and should not be instantiated. TypeParser contains a static dictionary which organizes available TypeRules by their associated Connector to minimize iteration over non-matching TypeRules.

# TypeParser.determineExpressionType() takes a starting Node and Variable type dictionary as arguments and performs a recursive depth-first search starting at the argument Node to determine the type of the whole expression from the bottom up. It uses the passed-in Variable type dictionary (Variables as keys, Types as values) to convert Variables to Types as necessary.

# class TypeParser:

#     _TYPE_RULES is a dictionary which sorts all available TypeRules by their input lengths (1, 2, and 3)

#     IMPORT_TYPES(variable_types, typerule_list):
#         For each variable type and type rule in the input lists
#             Create a new TypeRule instance for this rule
#             Sort the new instance into the TYPE_RULES dictionary by input length
#         Add a final [["(", "*", ")"], "*"] rule into the TYPE_RULES.3 at the end to handle parentheses-enclosed single types
#         Add a final [["*"], "*"] rule into the TYPE_RULES.1 at the end to handle conversions of types into themselves (simplifies parsing)

#     _TYPE(input_token_list):
#         For each TypeRule in the TYPE_RULES for the input list's length
#             If the current TypeRule.APPLY() does not return None, return its returned type

#         Return None if execution has not yet found a matching TypeRule

#     EXPRESSION_TYPE(Node)
#         If Node has no children
#             return _SUBEXPRESSION_TYPE(Node.to_list())
#         Else
#             Store the output of _CHILD_TYPES(Node.children()) in child_types
#             While child_types has length > 1
#                 Store _NEXT_EXPRESSION(child_types) in next_expression
#                 Store _SUBEXPRESSION_TYPE(next_expression) in next_expression_type
#                 Prepend child_types with next_expression_type

#     _SUBEXPRESSION_TYPE(expression):
#         For each TypeRule matching the expression's length
#             Attempt to apply this TypeRule to our expression.
#             If output of TypeRule.apply() is not None, RETURN it immediately.
#         Return None, since we failed to match any TypeRule.

#     _CHILD_TYPES(children):
#         Initialize child_types to an empty list
#         For each child of this Node
#             Append EXPRESSION_TYPE(child) to child_types
#         return child_types

#     _NEXT_EXPRESSION(child_types):
#         Initialize expression to an empty list
#         While expression length < 3
#             If _HAS_UNARY_NEGATION(expression, child_types)
#                 Add _SUBEXPRESSION_TYPE(child_types[:2]) to expression
#                 Pop next two elements from child_types
#             Else
#                 Add next child type to expression
#                 Pop next element from child_types
#         Return expression

#     _HAS_UNARY_NEGATION(expression, child_types):
#         Return True If (expression length is 0 or 2) and next child type is MINUS
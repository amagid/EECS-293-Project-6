# Typed Parser Design Document

The fundamental idea behind this algorithm is to take a valid parse tree and perform a depth-first search of the expressions, determining each one's type from the ground up.

## Classes & Enums

#### TypeRule Class

Instances of the TypeRule class define how to determine the type of an expression structure. A TypeRule has an internally-stored list of string representations, as well as an internally-stored string type output. TypeRules are generic by design, but have a few restrictions on their input and output tokens:
- There must be **exactly one** string output token - an expression must become a type, not another expression.
- There must be **one, two, or three** string input tokens.
- If there is only one string input token, it **must not** be equal to the string output token.
- If there are two string input tokens, the first **must** be MINUS and the second **must** be a type.
- If there are three string input tokens, the first and third **must** be types and the middle **must** be a connector.

The TypeRule exposes a TypeRule.apply(Node) method which returns the type resulting from applying the given TypeRule on the expression rooted at Node, as well as the number of tokens that were matched. This method returns None if the TypeRule cannot be applied to this Node.

class TypeRule:
    INIT(input_types, output_type):
        Store the input and output types internally, assert that they are all valid including in their organization

    APPLY(input_token_list):
        If the input_token_list matches this TypeRule's input token list, return this TypeRule's output type
        Else, return None

#### TypeParser Class

This is the entry point of the application. TypeParser provides a static entry method, determineExpressionType, and should not be instantiated. TypeParser contains a static dictionary which organizes available TypeRules by their associated Connector to minimize iteration over non-matching TypeRules.

TypeParser.determineExpressionType() takes a starting Node and Variable type dictionary as arguments and performs a recursive depth-first search starting at the argument Node to determine the type of the whole expression from the bottom up. It uses the passed-in Variable type dictionary (Variables as keys, Types as values) to convert Variables to Types as necessary.

class TypeParser:

    _TYPE_RULES is a dictionary which sorts all available TypeRules by their input lengths (1, 2, and 3)

    IMPORT_TYPES(variable_types, typerule_list):
        For each variable type and type rule in the input lists
            Create a new TypeRule instance for this rule
            Sort the new instance into the TYPE_RULES dictionary by input length
        Add a final [["(", "*", ")"], "*"] rule into the TYPE_RULES.3 at the end to handle parentheses-enclosed single types
        Add a final [["*"], "*"] rule into the TYPE_RULES.1 at the end to handle conversions of types into themselves (simplifies parsing)

    _TYPE(input_token_list):
        For each TypeRule in the TYPE_RULES for the input list's length
            If the current TypeRule.APPLY() does not return None, return its returned type

        Return None if execution has not yet found a matching TypeRule

    EXPRESSION_TYPE(Node)
        If Node has no children
            return _SUBEXPRESSION_TYPE(Node.to_list())
        Else
            Store the output of _CHILD_TYPES(Node.children()) in child_types
            While child_types has length > 1
                Store _NEXT_EXPRESSION(child_types) in next_expression
                Store _SUBEXPRESSION_TYPE(next_expression) in next_expression_type
                Prepend child_types with next_expression_type

    _SUBEXPRESSION_TYPE(expression):
        For each TypeRule matching the expression's length
            Attempt to apply this TypeRule to our expression.
            If output of TypeRule.apply() is not None, RETURN it immediately.
        Return None, since we failed to match any TypeRule.

    _CHILD_TYPES(children):
        Initialize child_types to an empty list
        For each child of this Node
            Append EXPRESSION_TYPE(child) to child_types
        return child_types

    _NEXT_EXPRESSION(child_types):
        Initialize expression to an empty list
        While expression length < 3
            If _HAS_UNARY_NEGATION(expression, child_types)
                Add _SUBEXPRESSION_TYPE(child_types[:2]) to expression
                Pop next two elements from child_types
            Else
                Add next child type to expression
                Pop next element from child_types
        Return expression

    _HAS_UNARY_NEGATION(expression, child_types):
        Return True If (expression length is 0 or 2) and next child type is MINUS
            
        

## Error Handling

The general error handling approach is to encapsulate the validity or invalidity of a given expression via the None enum member. As the TypeParser searches the parse tree, each time it finds a parsable expression part (a Node where all direct children have defined Types), it will pass this Node into its TypeRules. If no suitable Type can be determined, the Type will be INVALID, thereby blocking most errors from bubbling up immediately. The TypeParser will be somewhat robust, allowing for the addition of type rules that include INVALID types as inputs. However, if no such rules are defined or matched, INVALID types will inevitably bubble up and cause the root type to be INVALID. This will inherently gracefully handle most errors.

## Testing Approach

The fundamental approach to testing here will be to ensure that every method is unit tested at least to 100% code coverage and to all input edge cases, with comprehensive integration testing covering many different expression trees and unorthodox type rules.
# Typed Parser Design Document

The fundamental idea behind this algorithm is to take a valid parse tree and perform a depth-first search of the expressions, determining each one's type from the ground up.

## Classes & Enums

#### Type Enum

The Type enum lists the available types in the system. There are no restrictions given on the number or specifications of the types in this enum. It merely provides a symbolic representation of the types.

The Type Enum contains an additional INVALID type which is used when no TypeRule can be matched to a given expression part.

class Type(Enum):
    INT = 1
    STRING = 2
    etc...

#### TypeRule Class

Instances of the TypeRule class define how to determine the type of an expression structure. A TypeRule has an internally-stored Connector and one or two Types representing the types of the operands to the Connector.

The TypeRule exposes a TypeRule.apply(Node) method which returns the Type resulting from applying the given TypeRule on the expression rooted at Node. This method returns Type.INVALID if the TypeRule cannot be applied to this Node.

class TypeRule:
    INIT(connector, operand_types, output_type):
        store the connector, operand, and output types internally, assert that they are all valid

    APPLY(Node, operand_types):
        if this Node is an InternalNode containing this TypeRule's internally stored Connector and its operands' types match the required types for this TypeRule, return this TypeRule's output_type.
        Else, return Type.INVALID

#### TypeParser Class

This is the entry point of the application. TypeParser provides a static entry method, determineExpressionType, and should not be instantiated. TypeParser contains a static dictionary which organizes available TypeRules by their associated Connector to minimize iteration over non-matching TypeRules.

TypeParser.determineExpressionType() takes a starting Node and Variable type dictionary as arguments and performs a recursive depth-first search starting at the argument Node to determine the type of the whole expression from the bottom up. It uses the passed-in Variable type dictionary (Variables as keys, Types as values) to convert Variables to Types as necessary.

class TypeParser:
    DETERMINE_EXPRESSION_TYPE(Node, variable_types, connector_type_rules):
        Store variable_types internally
        Store connector_type_rules internally
        Return the output of _SUBTREE_TYPE(Node)

    _SUBTREE_TYPE(Node)
        Store the output of _CHILD_TYPES(Node) in child_types
        Look up the list of potential TypeRules in connector_type_rules dictionary based on this Node's Connector
        For each potential TypeRule
            Attempt to apply this TypeRule to our Node and its child_types.
            If output of TypeRule.apply() is not Type.INVALID, RETURN it immediately.
        Return Type.INVALID, since we failed to match any TypeRule.

    _CHILD_TYPES(Node):
        Initialize child_types to an empty list
        For each child of this Node
            If the child is a leaf node, get its type from _LEAF_TYPE()
            If the child is an internal node, call _SUBTREE_TYPE() on it and store the output in child_types

    _LEAF_TYPE(Node, variable_types):
        Look up this Node in the variable_types dictionary. If the Node is contained there, return the associated Type.
        Else, return Type.INVALID

## Error Handling

The general error handling approach is to encapsulate the validity or invalidity of a given expression via the Type.INVALID enum member. As the TypeParser searches the parse tree, each time it finds a parsable expression part (a Node where all direct children have defined Types), it will pass this Node into its TypeRules. If no suitable Type can be determined, the Type will be INVALID, thereby blocking most errors from bubbling up immediately. The TypeParser will be somewhat fail-fast, meaning that if it encounters an INVALID expression, it will cancel its search and return the INVALID type for the input expression as a whole. This will stop any errors from causing cascading malfunctions in the parser.

## Testing Approach

The fundamental approach to testing here will be to ensure that every method is unit tested at least to 100% code coverage and to all input edge cases, with comprehensive integration testing covering many different expression trees and unorthodox type rules.
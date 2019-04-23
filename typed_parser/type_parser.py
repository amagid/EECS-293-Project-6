# This is the entry point of the application. TypeParser provides a static entry method, determineExpressionType, and should not be instantiated. TypeParser contains a static dictionary which organizes available TypeRules by their associated Connector to minimize iteration over non-matching TypeRules.

# TypeParser.determineExpressionType() takes a starting Node and Variable type dictionary as arguments and performs a recursive depth-first search starting at the argument Node to determine the type of the whole expression from the bottom up. It uses the passed-in Variable type dictionary (Variables as keys, Types as values) to convert Variables to Types as necessary.

from typed_parser.type_rule import TypeRule

class TypeParser:

    _type_rules = {
        1: [],
        2: [],
        3: []
    }

    def import_types(typerule_list, variable_types = []):
        all_type_rules = variable_types + typerule_list
        for type_rule in all_type_rules:
            self._type_rules[len(type_rule[0])].append(TypeRule(type_rule[0], type_rule[1]))
        # Add a final [["(", "*", ")"], "*"] rule into the TYPE_RULES.3 at the end to handle parentheses-enclosed single types
        # Add a final [["*"], "*"] rule into the TYPE_RULES.1 at the end to handle conversions of types into themselves (simplifies parsing)

    def expression_type(node)
        if not node.is_fruitful():
            return self._subexpression_type(node.to_list())
        else:
            child_types = self._child_types(node.get_children())
            while len(child_types) > 1:
                next_expression = self._next_expression(child_types)
                next_expression_type = self._subexpression_type(next_expression)
                child_types.insert(0, next_expression_type)

    def _subexpression_type(expression):
        for type_rule in self._type_rules[len(expression)]:
            applied_type = type_rule.apply(expression)
            if applied_type is not None:
                return applied_type
        return None

#     _child_types(children):
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
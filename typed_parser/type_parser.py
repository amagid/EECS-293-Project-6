# This is the entry point of the application. TypeParser provides a static entry method, determineExpressionType, and should not be instantiated. TypeParser contains a static dictionary which organizes available TypeRules by their associated Connector to minimize iteration over non-matching TypeRules.

# TypeParser.determineExpressionType() takes a starting Node and Variable type dictionary as arguments and performs a recursive depth-first search starting at the argument Node to determine the type of the whole expression from the bottom up. It uses the passed-in Variable type dictionary (Variables as keys, Types as values) to convert Variables to Types as necessary.

from typed_parser.type_rule import TypeRule

class TypeParser:

    #: _type_rules is used to keep track of all available type conversion
    #: rules. It is a dictionary containing lists of TypeRules, sorted by the
    #: length of their input patterns.
    _type_rules = {
        1: [],
        2: [],
        3: []
    }

    def __init__(self):
        """
        The TypeParser __init__ method is empty to allow for better testing.
        To use the TypeParser, create it, then run import_types, and then 
        run expression_type on a parse tree.
        """
        pass

    def import_types(self, typerule_list, variable_types = []):
        """
        import_types is used to parse and prepare the type rules that will be
        used in calculating the types of expression trees.
        This method takes two arguments:

        - *typerule_list*: A `list` of type rules, specified as:
            `[[input_types...], output_type]` Types should be specified as strings
        - *variable_types*: A `list` of variable types, in the same format as the
            type rules.
        """

        # For simplicity, variable types are treated exactly the same as type rules
        all_type_rules = variable_types + typerule_list

        # Sort all type rules by their input lengths into the _type_rules dict
        for type_rule in all_type_rules:
            self._type_rules[len(type_rule[0])].append(TypeRule(type_rule[0], type_rule[1]))

        # Add wildcard types as lowest priority for cleanup
        self._type_rules[1].append(TypeRule(['?'], '?'))
        self._type_rules[3].append(TypeRule(['(', '?', ')'], '?'))

    def expression_type(self, node):
        if not node:
            return None
        if not node.get_children():
            return self._subexpression_type(self._node_to_expression(node))
        else:
            child_types = self._child_types(node.get_children())
            while len(child_types) > 1:
                next_expression = self._next_expression(child_types)
                next_expression_type = self._subexpression_type(next_expression)
                child_types.insert(0, next_expression_type)
            return child_types[0]

    def _node_to_expression(self, node):
        expression = []
        for child in node.to_list():
            expression.append(str(child))
        return expression

    def _subexpression_type(self, expression):
        for type_rule in self._type_rules[len(expression)]:
            applied_type = type_rule.apply(expression)
            if applied_type is not None:
                return applied_type
        return None

    def _child_types(self, children):
        child_types = []
        for child in children:
            child_types.append(self.expression_type(child))
        return child_types

    def _next_expression(self, child_types):
        expression = []
        while len(expression) < 3:
            if self._has_unary_negation(child_types, expression):
                expression.append(self._subexpression_type(child_types[:2]))
                [child_types.pop(0) for _ in [0,1]]
            else:
                expression.append(child_types.pop(0))
        return expression

    def _has_unary_negation(self, child_types, expression):
        return len(expression) in [0,2] and child_types[0] == '-'
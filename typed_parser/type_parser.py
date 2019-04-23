from typed_parser.type_rule import TypeRule

class TypeParser:
    """
    This is the entry point of the application. TypeParser provides a static
    entry method, expression_type, and should not be instantiated. TypeParser
    contains a static dictionary which organizes available TypeRules by their
    associated input token lengths to minimize iteration over non-matching
    TypeRules. TypeParser.expression_type() takes a starting Node and Variable
    type dictionary as arguments and performs a recursive depth-first search
    starting at the argument Node to determine the type of the whole expression
    from the bottom up.
    """

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

        Params:

        - `list` *typerule_list* - A `list` of type rules, specified as: `[[input_types...], output_type]` Types should be specified as strings
        - `list` *variable_types* - A `list` of variable types, in the same format as the type rules.

        Returns:

        - `None`

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
        """
        expression_type is the main entry point for the package. Call
        TypeParser.expression_type and pass in a parse tree to have the root
        type of the tree calculated via a Depth-First Search of the tree.

        Params:

        - `InternalNode` *node* - Root node of a parse tree to reduce to a type

        Returns:
        
        - `string` - The root type of the parse tree
        
        """

        # End recursion & return this node's type if it is a leaf or nonexistent
        if not node:
            return None
        if not node.get_children():
            return self._subexpression_type(self._node_to_expression(node))
        else:
            # Iteratively consume expression to calculate the type of this node.
            # Recurse on complex children.
            child_types = self._child_types(node.get_children())
            while len(child_types) > 1:
                next_expression = self._next_expression(child_types)
                next_expression_type = self._subexpression_type(next_expression)
                child_types.insert(0, next_expression_type)
            return child_types[0]

    def _node_to_expression(self, node):
        """
        Convert a Node object into a more parse-friendly list of `string` type
        tokens. Assumes that all node children are leaf nodes.

        Params:

        - `Node` *node*

        Returns:

        - `list<string>`

        """

        expression = []
        for child in node.to_list():
            expression.append(str(child))
        return expression

    def _subexpression_type(self, expression):
        """
        Calculate the type of a leaf-level expression. That is, an expression
        with no complex child nodes that cannot be described by a single string
        type.

        Params:

        - `list<string>` *expression*

        Returns:

        - `string` - The type of the expression, if valid
        - `None` - None, if no type rules match the expression
        """

        # Return the first matched TypeRule's output type, or None if no match
        for type_rule in self._type_rules[len(expression)]:
            applied_type = type_rule.apply(expression)
            if applied_type is not None:
                return applied_type
        return None

    def _child_types(self, children):
        """
        Convert all nodes in an expression list to their associated types.
        This search handles the bulk of the parser's recursion, as it will
        start recursion on any node in the expression which is not a leaf node.

        Params:

        - `list<string>` *children* - The expression layer to parse

        Returns:

        - `list<string>` - The types of the original expression nodes
        """

        # Recursively determine types on each child node
        child_types = []
        for child in children:
            child_types.append(self.expression_type(child))
        return child_types

    def _next_expression(self, child_types):
        """
        Get the next valid simple expression from the current layer of the tree.
        This takes care of the iteration through simplified layers such as
        `a+b+c+d`, as it will first match `a+b`, then that `*result* +c`, and so on.

        Params:

        - `list<string>` *child_types* - The whole expression layer as a list of types

        Returns:

        - `list<string>` - The next valid simple expression
        """

        # Consume child_types from front to build expression
        expression = []
        while len(expression) < 3:
            # An expression can be longer than 3 tokens if some are unary-negated
            if self._has_unary_negation(child_types, expression):
                expression.append(self._subexpression_type(child_types[:2]))
                [child_types.pop(0) for _ in [0,1]]
            else:
                expression.append(child_types.pop(0))
        return expression

    def _has_unary_negation(self, child_types, expression):
        """
        Check whether the next part of the potential expression contains a unary negation.

        Params:

        - `list<string>` *child_types* - The expression that is being consumed and converted
        - 'list<string>` *expression* - The expression that is being built

        Returns:

        - `boolean`

        """
        
        return len(expression) in [0,2] and child_types[0] == '-'
import pytest
from typed_parser.non_terminal_symbol import NonTerminalSymbol, PRODUCTIONS
from typed_parser.symbol_sequence import SymbolSequence
from typed_parser.parse_state import ParseState
from typed_parser.variable import Variable
from typed_parser.connector import Connector
from typed_parser.terminal_symbol import TerminalSymbol
from typed_parser.utils import _str_to_token_list

# List of test cases for NTS parse test generator
# Format: (NonTerminalSymbol to test, Expression, Expect Success?)
TEST_EXPRESSIONS = [
    # Test FACTOR parse failure (state only) on empty list
    (NonTerminalSymbol.FACTOR, '', False),
    # Test FACTOR parse success (state only) of single-token list with a variable
    (NonTerminalSymbol.FACTOR, 'a', True),
    # Test FACTOR parse success (state only) of 3-token list with a variable in parentheses
    (NonTerminalSymbol.FACTOR, '(a)', True),
    # Test FACTOR parse success (state only) of many-token list wrapped in parentheses
    (NonTerminalSymbol.FACTOR, '(a+b/c)', True),
    # Test FACTOR failure (state only) on many-token list not wrapped in parentheses
    (NonTerminalSymbol.FACTOR, '-a+b/c', False),
    
    # Test UNARY failure (state only) on empty list
    (NonTerminalSymbol.UNARY, '', False),
    # Test UNARY parse success (state only) of single-token list with a variable
    (NonTerminalSymbol.UNARY, 'a', True),
    # Test UNARY parse success (state only) of two-token list with unary negation of a variable
    (NonTerminalSymbol.UNARY, '-a', True),
    # Test UNARY parse success (state only) of many-token list with an expression wrapped in parentheses
    (NonTerminalSymbol.UNARY, '(a+b)', True),
    # Test UNARY parse success (state only) of many-token list with unary negation of expression wrapped in parentheses
    (NonTerminalSymbol.UNARY, '-(a+b)', True),
    # Test UNARY failure (state only) on term_tail two-token list [+, a]
    (NonTerminalSymbol.UNARY, '+a', False),

    # Test TERM_TAIL parse success (state only) of empty list
    (NonTerminalSymbol.TERM_TAIL, '', True),
    # Test TERM_TAIL parse success (state only) of two-token list with variable multiplication
    (NonTerminalSymbol.TERM_TAIL, '*a', True),
    # Test TERM_TAIL parse success (state only) of two-token list with variable division
    (NonTerminalSymbol.TERM_TAIL, '/a', True),
    # Test TERM_TAIL parse success (state only) of many-token list beginning with variable multiplication
    (NonTerminalSymbol.TERM_TAIL, '*a+b', True),

    # Test TERM failure (state only) on empty list
    (NonTerminalSymbol.TERM, '', False),
    # Test TERM parse success (state only) of single-token list with variable
    (NonTerminalSymbol.TERM, 'a', True),
    # Test TERM parse success (state only) of three-token list with variable multiplication by variable
    (NonTerminalSymbol.TERM, 'a*b', True),
    # Test TERM parse success (state only) of four-token list with unary negation in variable multiplication
    (NonTerminalSymbol.TERM, '-a*b', True),
    # Test TERM failure (state only) on many-token list beginning with non-negation operator [+, *, /]
    (NonTerminalSymbol.TERM, '+a*b/c', False),

    # Test EXPRESSION_TAIL parse success (state only) of empty list
    (NonTerminalSymbol.EXPRESSION_TAIL, '', True),
    # Test EXPRESSION_TAIL parse success (state only) of two-token list with variable addition
    (NonTerminalSymbol.EXPRESSION_TAIL, '+a', True),
    # Test EXPRESSION_TAIL parse success (state only) of two-token list with variable subtraction
    (NonTerminalSymbol.EXPRESSION_TAIL, '-a', True),
    # Test EXPRESSION_TAIL parse success (state only) of three-token list with double-negative variable
    (NonTerminalSymbol.EXPRESSION_TAIL, '--a', True),
    # Test EXPRESSION_TAIL parse success (state only) of many-token list with addition of complex sub-expression
    (NonTerminalSymbol.EXPRESSION_TAIL, '+(a-b/(c*d))', True),
    
    # Test EXPRESSION failure on empty list
    (NonTerminalSymbol.EXPRESSION, '', False),
    # Test EXPRESSION parse of single-token list with variable
    (NonTerminalSymbol.EXPRESSION, 'a', True),
    # Test EXPRESSION parse of two-token list with unary negation of variable
    (NonTerminalSymbol.EXPRESSION, '-a', True),
    # Test EXPRESSION parse of many-token list with variable in parentheses
    (NonTerminalSymbol.EXPRESSION, '(a)', True),
    # Test EXPRESSION parse of many-token list with variable multiplication and then division in parentheses
    (NonTerminalSymbol.EXPRESSION, '(a*b/c)', True),
    # Test EXPRESSION parse of many-token list with variable addition and subtraction
    (NonTerminalSymbol.EXPRESSION, 'a+b-c', True),
    # Test parse of assignment example input [a+b/c]
    (NonTerminalSymbol.EXPRESSION, 'a+b/c', True)
]

# Helper method to extract and format data from a TEST_EXPRESSION test case
def _extract_from_test_expression(test_expr):
    return test_expr[0], _str_to_token_list(test_expr[1]), test_expr[2]

# Parametrize test to generate matching tests for all NonTerminalSymbols
@pytest.mark.parametrize(
    'test_expr', TEST_EXPRESSIONS
)
# Test various cases of specific NonTerminalSymbols attempting to parse expressions
def test_parse_by_sub_nts_types(test_expr):
    nts, expr, expected = _extract_from_test_expression(test_expr)
    state = nts.parse(expr)

    assert state.success() == expected

# Test EXPRESSION error on None list
def test_parse_error_on_none_list():
    with pytest.raises(ValueError):
        NonTerminalSymbol.parse_input(None)

# Test _get_next_production when token_list is empty
def test_get_next_production_empty_list():
    token_list = []
    result = NonTerminalSymbol.EXPRESSION._get_next_production(token_list)

    assert result is PRODUCTIONS[NonTerminalSymbol.EXPRESSION][None]

# Test _get_next_production when token_list has tokens in it
def test_get_next_production_populated_list():
    token_list = [Connector.build(TerminalSymbol.OPEN)]
    result = NonTerminalSymbol.EXPRESSION._get_next_production(token_list)

    assert result is PRODUCTIONS[NonTerminalSymbol.EXPRESSION][TerminalSymbol.OPEN]
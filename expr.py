"""
Expressions.  An expression is a subtree, which may be
- a numeric value, like 5
- a named variable, like x
- a binary operator, like 'plus', with a left and right subtree

Expressions are interpreted in an environment, which is a
mapping from variable names to values. A variable may evaluate
to its value if its name is mapped to its value in the environment.
"""

# A memory for our calculator
from calc_state import Env

# In Python number hierarchy, Real is the
# common superclass of int and float
from numbers import Real

# Debugging aids 
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)



class Expr(object):
    """Abstract base class. Cannot be instantiated."""

    def eval(self, env: Env):
        """Each concrete subclass of Expr must define this method,
        which evaluates the expression in the context of the environment
        and returns the result.
        """
        raise NotImplementedError(
            "No eval method has been defined for class {}".format(type(self)))


class Var(Expr):
    """A variable has a name and may have a value in the environment."""

    def __init__(self, name):
        """Expression is reference to a variable named name"""
        assert isinstance(name, str)
        self.name = name

    def eval(self, env: Env):
        """Fetches value from environment."""
        log.debug("Evaluating {} in Var".format(self))
        val = env.get(self.name)
        return val

    def __repr__(self):
        return "Var('{}')".format(self.name)

    def __str__(self):
        return self.name


class Const(Expr):
    """An expression that is just a constant value, like 5"""

    def __init__(self, value):
        assert isinstance(value, Real)
        self.val = value

    def eval(self, env: Env):
        """This is about as evaluated as it can get"""
        log.debug("Evaluating {} in Const".format(self))
        return self

    def value(self):
        """The internal value"""
        return self.val

    def __repr__(self):
        return "Const({})".format(self.val)

    def __str__(self):
        return str(self.val)

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.val == other.val


class Assign(Expr):
    """let x = Expr.  We treat an assignment as an expression
    that returns the value of the right-hand side, but usually
    assignments are evaluated for side effect on the
    environment.
    """

    def __init__(self,  expr: Expr, var: Var):
        """Representation of 'let var = expr'"""
        assert isinstance(var, Var)
        assert isinstance(expr, Expr)
        self.var = var
        self.expr = expr

    def __repr__(self):
        return "Assign({},{})".format(self.var, self.expr)

    def __str__(self):
        return "let {} = {}".format(self.var, self.expr)

    def eval(self, env: Env) -> Expr:
        """Stores value of expr evaluated in environment
        and returns that value.
        """
        log.debug("Evaluating {} in Assign".format(self))
        val = self.expr.eval(env)
        log.debug("Assigning {} <- {}".format(self.var.name, val))
        env.put(self.var.name, val)
        return val


# class BinOp(Expr):
#     """Abstract superclass for binary expressions like plus, minus.
#     These operations apply to numeric constants (Const nodes) and
#     return numeric constants.
#     """
#
#     def __init__(self, left, right):
#         """A binary operation has a left and right sub-expression"""
#         assert isinstance(left, Expr)
#         assert isinstance(right, Expr)
#         self.left = left
#         self.right = right
#
#     def eval(self, env: Env):
#         """Evaluation strategy for binary operations
#         that apply to numbers and produce numbers.
#         """
#         log.debug("Evaluating {} in BinOp".format(self))
#         lval = self.left.eval(env)
#         assert isinstance(lval, Const), "Op {} applies to numbers, not to {}".format(
#           type(self).__name__, lval)
#         lval_n = lval.value()
#         rval = self.right.eval(env)
#         assert isinstance(lval, Const), "Op {} applies to numbers, not to {}".format(
#           type(self).__name__, rval)
#         rval_n = rval.value()
#         return Const(self._apply(lval_n, rval_n))
#
#     def _apply(self, left: Real, right: Real) -> Real:
#         """Apply operation to numeric values.  Each concrete
#         subclass of BinOp must define this method.
#         Note: In Python, 'int' and 'float' are subtypes of Real.
#         """
#         raise NotImplementedError(
#             "Class {} has not defined its _apply method".format(type(self)))
#
#     def __eq__(self, other):
#         """Identical expression"""
#         return isinstance(self, type(other)) \
#             and self.left == other.left \
#             and self.right == other.right
#
#
# class Plus(BinOp):
#     """Represents the expression A + B"""
#
#     def _apply(self, left: Real, right: Real) -> Real:
#         """Addition of two numeric values (Const nodes)"""
#         return left + right
#
#     def __repr__(self):
#         return "Plus({},{})".format(repr(self.left), repr(self.right))
#
#     def __str__(self):
#         """Print fully parenthesized"""
#         return "({} + {})".format(self.left, self.right)
#
#
# class Minus(BinOp):
#     """Represents the expression A - B"""
#
#     def _apply(self, left: Real, right: Real) -> Real:
#         """Subtraction of two numbers (int or float)"""
#         return left - right
#
#     def __repr__(self):
#         return "Minus({},{})".format(repr(self.left), repr(self.right))
#
#     def __str__(self):
#         """Print fully parenthesized"""
#         return "({} - {})".format(self.left, self.right)
#
#
# class Times(BinOp):
#     """Represents the expression A * B"""
#     # __init__ is inherited from BinOp
#
#     def _apply(self, left: Real, right: Real):
#         """Addition of two numeric values"""
#         return left * right
#
#     def __repr__(self):
#         return "Times({},{})".format(repr(self.left), repr(self.right))
#
#     def __str__(self):
#         """Print fully parenthesized"""
#         return "({} * {})".format(self.left, self.right)
#
#
# class Div(BinOp):
#     """Exact division (not truncating) of two numeric values"""
#
#     def _apply(self, left: Real, right: Real):
#         """Addition of two numeric values (Const nodes)"""
#         return left / right
#
#     def __repr__(self):
#         return "Div({},{})".format(repr(self.left), repr(self.right))
#
#     def __str__(self):
#         """Print fully parenthesized"""
#         return "({}/{})".format(self.left, self.right)
#

class UnOp(Expr):
    """Abstract superclass for unary expressions like negation"""

    def __init__(self, left: Expr):
        """A unary operation has only a left  sub-expression"""
        assert isinstance(left, Expr)
        self.left = left

    def eval(self, env: Env) -> Const:
        """Evaluation strategy for unary expressions"""
        log.debug("Evaluating {} in UnOp".format(self))
        lval = self.left.eval(env)
        assert isinstance(lval, Const), "Op {} applies to numbers, not to {}".format(
            type(self).__name__, lval)
        lval_n = lval.value()
        return Const(self._apply(lval_n))

    def _apply(self, val: Real) -> Real:
        raise NotImplementedError("Class {} has not implemented _apply".format(
            type(self).__name__))


class Neg(UnOp):
    """Numeric negation"""
    
    def _apply(self, val: Real) -> Real:
        """Negation of a numeric value"""
        return 0 - val

    def __repr__(self):
        return "Neg({})".format(repr(self.left))

    def __str__(self):
        """Print fully parenthesized"""
        return "~{}".format(self.left)

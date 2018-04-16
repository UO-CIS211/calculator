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


class UnOp(Expr):
    """Abstract superclass for unary expressions like negation"""

    def __init__(self, left: Expr):
        """A unary operation has only a left  sub-expression"""
        assert isinstance(left, Expr)
        self.left = left

    def __eq__(self, other):
        """Identical expression"""
        return type(self) == type(other) \
            and self.left == other.left 

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

# FIXME:  We also need binary operators.  You need an abstract class
# BinOp and a set of concrete subclasses Plus, Minus, Times, Div

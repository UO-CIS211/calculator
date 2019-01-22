"""
An LL parser for the CIS 211 calculator.
Michal Young, spring 2018, revised winter 2019

LL / recursive descent parsing is one of approach to
parsing syntax of programming languages, including
arithmetic expressions.   I'll describe this more
in a separate document
"""

from lex import TokenStream, TokenCat
import expr
import io
from typing import TextIO

import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class InputError(Exception):
    """Raised when we can't parse the input"""
    pass


def parse(srcfile: TextIO) -> expr.Expr:
    """Interface function to LL parser"""
    stream = TokenStream(srcfile)
    return _program(stream)

#
# The grammar comes here.  We will have a similar parser
# with a richer grammar for a programming langauge we will
# compile in our last project.  This grammar just parses
# one expression or assignment.
#
#  program ::= stmt
#  stmt ::= exp ['=' exp]
#  exp ::= term { ('+'|'-') term }
#  term ::= primary { ('*'|'/')  primary }
#  primary ::= IDENT | CONST | '(' exp ')'
#


def require(stream: TokenStream, category: TokenCat, desc: str = "", consume=False):
    """Requires the next token in the stream to match a specified category.
    Consumes and discards it if consume==True.
    """
    if stream.peek().kind != category:
        raise InputError(f"Expecting {desc or category}, but saw {stream.peek()} instead")
    if consume:
        stream.take()
    return


def _program(stream: TokenStream) -> expr.Expr:
    """
    program ::= stmt

    We are parsing just a single statement for the
    calculator.  Later we will parse a sequence of
    statements in programs.
    """
    log.debug(f"Parsing program from token {stream.peek()}")
    return _stmt(stream)

def _stmt(stream: TokenStream) -> expr.Expr:
    """
    stmt ::= exp ['=' exp]
    """
    left = _expr(stream)
    if stream.peek().kind is TokenCat.ASSIGN:
        if not isinstance(left, expr.Var):
            raise InputError("Can only assign to a variable")
        stream.take()
        right = _expr(stream)
        return expr.Assign(left, right)
    else:
        return left


def _expr(stream: TokenStream) -> expr.Expr:
    """
    expr ::= term { ('+'|'-') term }
    """
    log.debug(f"parsing sum starting from token {stream.peek()}")
    left = _term(stream)
    log.debug(f"sum begins with {left}")
    while stream.peek().value in ["+", "-"]:
        op = stream.take()
        log.debug(f"expr addition op {op}")
        right = _term(stream)
        if op.value == "+":
            left = expr.Plus(left, right)
        elif op.value == "-":
            left = expr.Minus(left, right)
        else:
            raise InputError(f"What's that op? {op}")
    return left


def _term(stream: TokenStream) -> expr.Expr:
    """term ::= primary { ('*'|'/')  primary }"""
    left = _primary(stream)
    log.debug(f"term starts with {left}")
    while stream.peek().value in ["*", "/"]:
        op = stream.take()
        right = _primary(stream)
        if op.value == "*":
            left = expr.Times(left, right)
        elif op.value == "/":
            left = expr.Div(left, right)
        else:
            raise InputError(f"Expecting multiplicative op, got {op}")
    return left


def _primary(stream: TokenStream) -> expr.Expr:
    """Constants, Variables, and parenthesized expressions"""
    log.debug(f"Parsing primary with starting token {stream.peek()}")
    token = stream.take()
    if token.kind is TokenCat.INT:
        log.debug(f"Returning Const node from token {token}")
        return expr.IntConst(int(token.value))
    elif token.kind is TokenCat.VAR:
        log.debug(f"Variable {token.value}")
        return expr.Var(token.value)
    elif token.kind is TokenCat.LPAREN:
        nested = _expr(stream)
        require(stream, TokenCat.RPAREN, consume=True)
        return nested
    else:
        raise InputError(f"Confused about {token} in expression")

###
# Calculator
###

def calc(text: str):
    """Parse and execute a single line"""
    try:
        exp = parse(io.StringIO(text))
        print(f"{exp} => {exp.eval()}")
    except Exception as e:
        print(f"Oops! {e}")

def llcalc():
    """Interactive calculator interface."""
    txt = input("Expression (return to quit):")
    while len(txt.strip()) > 0:
        calc(txt)
        txt = input("Expression (return to quit):")
    print("Bye! Thanks for the math!")


if __name__ == "__main__":
    llcalc()
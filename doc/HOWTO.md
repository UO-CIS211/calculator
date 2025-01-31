# Howto:  Calculator

In this project we're going to create a calculator.  Actually my 
plan is to create two different calculators, with some shared 
core functionality.  You will build the shared core functionality 
(a module ```expr.py``` with classes representing 
arithmetic expressions) and one of the two calculators that use it. 

One of the two calculators will take a conventional algebraic notation, 
e.g., ```( 5 + 3 ) * 4``` should produce `32`. I will provide the 
_parser_ that converts an expression like ```(5+3)*4``` into a _tree_,
and you will provide the methods for calculating the result `32` 
from the tree. The other calculator will take 
reverse Polish notation (RPN), also called _postfix_, in which we 
would write the same 
expression as ```5 3 + 4 *```.   You will provide the code for 
translating this postfix expression into the same tree form. 

There will be two main parts.  `expr.py` will define the classes for 
nodes of expression trees.  The classes defined in `expr.py` will be 
used by both versions of the calculator.  `rpncalc.py` will be the 
calculator for reverse Polish notation. 

## Expressions

We want to represent expressions as objects. Expressions we want to 
represent include: 

* Integer constants, like 5.  The value of an integer constant
is itself.   This will be class IntConst, and we'll create it 
with a call like ```IntConst(5)```

* Variables, like x.  Our calculator will allow us to assign 
values to variables.  The value of a variable is whatever value
it is currently holding.  (More on this below.)

* Operations. There are a few kinds of these. 

    * Binary operations are like ```+``` and ```*```.  We call 
    them 'binary' because they have two operands.  For example, 
    we might create the representation of ```5 + 3``` as 
    ```Plus(IntConst(5), IntConst(3))```.  The value 
    of a binary operation is found by applying an 
    operation to the values of its operands, e.g., 
    ```Plus(IntConst(5), IntConst(3)).eval()``` would 
    return ```IntConst(8)```. 
    
    * Unary operations like absolute value.  These are operations 
    that have only a single operand.  For example, we 
    might represent abs(3) (conventionally written 
    |3| in algebraic notation) as 
    ```Abs(IntConst(3))``` . 
    
    * Assignment.  When we add variables, we'll 
    want to add an operation for assigning a 
    value to a variable, e.g., x = 3 
    would be ```Assign(Var('x'), IntConst(3))``` 
    
    
Our plan is to have a single *abstract* class ```Expr``` and make
all kinds of expressions like ```IntConst``` and ```Plus``` be 
subclasses of ```Expr```.   All subclasses of ```Expr``` should implement
an ```eval``` method that returns the value obtained by 
evaluating the expression.  For example, the expression 

```python
Times(Plus(IntConst(5), IntConst(3)), IntConst(4)).eval()
```
should return `IntConst(32)`.  

In addition to `eval`, we would like each kind of expression to 
have a ```__str__``` method to return its customary string 
representation in algebraic notation
and ```__repr__``` to return a string that looks 
like a call to construct the expression.  For example, 
```python
str(Times(Plus(IntConst(5), IntConst(3)), IntConst(4)))
```
should return "(5+3)*4" and 
```python
repr(Times(Plus(IntConst(5), IntConst(3)), IntConst(4)))
```
should return "Times(Plus(IntConst(5), IntConst(3)), IntConst(4))". 

Getting minimal parentheses in the ```__str__``` method 
is a bit complicated, so our ```__str__``` method will 
over-parenthesize expressions with binary operations.  
Unary operations do not present the same issues of 
ambiguity, so we will not need additional parentheses for 
negation and absolute value. 

## expr.py

Create file `expr.py`, the source code file that will hold all the 
classes for representing expression trees. Give it a header 
docstring in the usual way. 

### Class Expr

We start with the abstract base class Expr.  It serves as 
a template and documentation for concrete subclasses, stating
that each one should implement ```eval```, ```__str__```, and 
```__repr__```. 

```python
class Expr(object):
    """Abstract base class of all expressions."""

    def eval(self) -> "IntConst":
        """Implementations of eval should return an integer constant."""
        raise NotImplementedError(
            f"'eval' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define 'eval'")

    def __str__(self) -> str:
        """Implementations of __str__ should return the expression in algebraic notation"""
        raise NotImplementedError(
            f"'__str__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__str__'")

    def __repr__(self) -> str:
        """Implementations of __repr__ should return a string that looks like
        the constructor, e.g., Plus(IntConst(5), IntConst(4))
        """
        raise NotImplementedError(
            f"'__repr__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__repr__'")
```

There are a couple of new things to note in the error messages these 
abstract methods produce.   
First is the way they access name of the class of an object `t` as
`t.__class__.__name__`.  `t.__class__` obtains the class of object 
`t`, and `__name__` gets the name of that class as a string.  Second 
is that the error message is broken across two lines just by giving a
sequence of string literals.  In Python,
`"First part,"   " second part"` concatenates the two string literals to
give us `"First part, second part"`. 

### Checkpoint 1

At this point you have `expr.py` with one abstract class, `Expr`.
You can test this by starting a Python console in the terminal.
Import the `Expr` class from `expr.py`, create an `Expr` object
and attempt to print it. 

```commandline
$ python3
Python 3.10.2 (v3.10.2:a58ebcc701, Jan 13 2022, 14:50:16) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from expr import Expr
>>> e = Expr()
>>> print(e)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/michal/Dropbox/23W-211/projects/dist/calculator/expr.py", line 14, in __str__
    raise NotImplementedError(
NotImplementedError: '__str__' not implemented in Expr
Each concrete Expr class must define '__str__'
```

(While this should work in any Python 3 console, as of January 2023
PyCharm has a bug that prevents display of the "NotImplementedError" 
message in the PyCharm console.)

### IntConst

The first concrete subclass we will build is ```IntConst```,
because it is the return type of ```eval``` and we really can't test 
anything else without it.   We'll start by creating a 
file ```test_expr.py``` and writing a couple of test cases for it. 

Here's a start: 

```python
"""Unit tests for expr.py"""

import unittest
from expr import *

class TestIntConst(unittest.TestCase):

    def test_eval(self):
        five = IntConst(5)
        self.assertEqual(five.eval(),IntConst(5))

    def test_str(self):
        twelve = IntConst(12)
        self.assertEqual(str(twelve), "12")

    def test_repr(self):
        forty_two = IntConst(42)
        self.assertEqual(repr(forty_two), f"IntConst(42)")

if __name__ == "__main__":
    unittest.main()
```

Next we write the actual class, filling in the needed methods in the 
usual way.  You will need to create class IntConst 
and methods `__init__`, `eval`, `__str__`, and `__repr__`. 
An `IntConst` object should have one instance variable, 
an `int` value. It should have the same string representation 
as the `int` value it wraps.  It's `repr` should look 
  like a call to the `IntConst` constructor. 
  An `IntConst` evaluates to 
itself, i.e., the `eval` method can just `return self`. 

When you have written the `IntConst` class, 
run the tests again.  
Perhaps you have already guessed what error we will see.  If not, 
it will look a little puzzling: 

```
FAIL: test_eval (__main__.TestIntConst)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/michal/DropBox/19W-211/projects/dev/recalc/test_expr.py", line 10, in test_eval
    self.assertEqual(five.eval(),IntConst(5))
AssertionError: IntConst(5) != IntConst(5)
```

We expected IntConst(5) and we got IntConst(5), but they are rejected 
as not being equal.  We certainly expect that those two values 
should be equal, but the built-in equality considers them different
because they are two distinct objects, even if they are identical. 

The fix is fairly straightforward:  We need to add a ```__eq__``` 
method to `IntConst`. 
The obvious 
implementation might be: 

```python
    def __eq__(self, other: Expr):
        return self.value == other.value
```

However, this isn't right, because we need to be
able to compare any `Expr` object to any other. 
Consider: 

```python
IntConst(7) == Plus(IntConst(3), IntConst(4))
```

This should return `False` (it is not the same tree, even if it
would evaluate to the same value), but it would instead raise an 
exception because a `Plus` object does not have a `value` field 
(instance variable). 

What should we do?  Python provides the ```isinstance``` 
function to check whether an object belongs to 
some class. We'll make use of it so that we 
only access the instance variables of `other` if 
it is in fact an `IntConst`.  Objects of different types will never
be considered equal: 

```python
    def __eq__(self, other: Expr):
        return isinstance(other, IntConst) and self.value == other.value
```

Using this definition, our tests so far should succeed: 

```python
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```

### Checkpoint

At this point your `expr.py` file contains the abstract class `Expr` 
and the concrete subclass `IntConst`.  Your `test_expr.py` contains 
test cases for `IntConst`. 

### Question (answer in questions.md)
Consider the following code. 
```python
five = IntConst(5)
print(5 == five)   # Comparison 1
print(five == 5)   # Comparison 2
```

Does the `__eq__` method of `IntConst` get called only in Comparison 
1, only in Comparison 2, in both, or in neither? 

### Plus

We'll start with one binary operation, 
`Plus` (represented by "+" in the input).  
Soon we will "refactor" this class, but it is often easiest to create 
a concrete example or maybe a couple of 
 concrete examples and only then consider what can be 
"factored out" into an abstract base class.  

We'll start with a couple of test cases for the ```__str__``` method. 

```python
class TestPlus(unittest.TestCase):
    
    def test_plus_str(self):
        exp = Plus(IntConst(5), IntConst(4))
        self.assertEqual(str(exp), "5 + 4")
        
     def test_nested_str(self):
        exp = Plus(Plus(IntConst(4), IntConst(5)), IntConst(3))
        self.assertEqual(str(exp), "((4 + 5) + 3)")
```

Even before we start to write code for actual ```Plus``` class, we can 
see that there is something tricky here.  How are we going to get 
parentheses around the nested sub-expression ```(5 + 4)``` but not
around the whole thing?  Maybe for ```Plus``` we could just omit all
the parentheses, but we couldn't do that for ```Minus```, because 
```(3 - 4) - 2``` is not the same as ```3 - (4 - 2)```. 
 
We could go to a lot of extra work to decide just where the
parentheses are really required, but that seems like too much
work for a simple calculator.  Will our user really mind so much if we
just put parentheses wherever they _might_ be needed?  We'll 
err on the side of over-parenthesization, and rewrite our 
test cases as follows: 

```python
class TestPlus(unittest.TestCase):

    def test_plus_str(self):
        exp = Plus(IntConst(5), IntConst(4))
        self.assertEqual(str(exp), "(5 + 4)")

    def test_nested_str(self):
        exp = Plus(Plus(IntConst(4), IntConst(5)), IntConst(3))
        self.assertEqual(str(exp), "((4 + 5) + 3)")
```

We'll also add some test cases for ```__repr__``` and ```__eq__```
and ```eval```, all within class `TestPlus`. 

```python
    def test_repr_simple(self):
        exp = Plus(IntConst(12), IntConst(13))
        self.assertEqual(repr(exp), "Plus(IntConst(12), IntConst(13))")

    def test_repr_nested(self):
        exp = Plus(IntConst(7), Plus(IntConst(4), IntConst(2)))
        self.assertEqual(repr(exp), "Plus(IntConst(7), Plus(IntConst(4), IntConst(2)))")

    def test_addition_simple(self):
        exp = Plus(IntConst(4), IntConst(8))
        self.assertEqual(exp.eval(), IntConst(12))

    def test_additional_nested(self):
        exp = Plus(IntConst(7), Plus(IntConst(2), IntConst(3)))
        self.assertEqual(exp.eval(), IntConst(12))
```

And now I can write the class ```Plus``` itself.   I'll leave the 
constructor to you ... it should store a left operand as ```self.left```
and a right operand as ```self.right```.

### ```__str__``` is recursive

The ```__str__``` method of ```Plus```
makes recursive calls on the ```__str__``` methods of the left 
and right operands: 

```python
    def __str__(self) -> str:
        """Algebraic notation, fully parenthesized: (left + right)"""
        return f"({self.left} + {self.right})"
```

How can this recursion work?  
If you haven't already, now would be a good time to 
read the [chapter](
https://uo-cs-oer.github.io/CS211-text/03_Recursion/03_1_Recursion.html)
on recursion in object-oriented programs.  As in ordinary 
functions, we must determine whether to apply the 
base case or the recursive case. But unlike in ordinary 
functions, the base case and the recursive case are not 
all together in a single function body, with an `if` statement
to select the appropriate code.  Instead, the base cases
and recursive cases are in different subclasses.  
 If we call 
```str``` on an ```IntConst``` object,
we get the base case.  If we call 
```str``` on a ```Plus``` object, 
we get the recursive case.  

The 
recursive case is still calling a "smaller" part of the original value. 
Just as in the pattern we used for recursive functions, at some 
point it will reach the base case and finish.  The structure of the 
recursive calls are echoed by the structure of the objects.  In fact 
we can (and often do) say that the expression structure is a 
*recursive data structure.* 

The ```__repr__``` method works much like the ```__str__``` method; 
I'll leave that to you to write. 


### Question (answer in questions.md)
I noted that `__str__` method of
`Plus` is recursive, but I don't see an explicit call to `__str__` 
in the code I provided.  Where is it? 

### Expressions are trees

One of the ways we can visualize an expression is as a tree.  
In software development and computer science we 
typically draw trees 
upside down, with the "root" or "root node" at the top and 
"leaves" or "leaf nodes" at the bottom.  (Occasionally 
we'll draw them sideways, with the root on the left 
and leaves on the right.)    The algebraic expression (3+4)*5 can be 
viewed as a tree with the operator "Times" at the top, connected to
subtrees for "Plus" (further connected to 3 and 4) on the left and 5 
on the right. 

![Image of tree as described just above, with "Times" at the top.
](img/Expr-Tree.png
"Expressions are trees")

Viewed this way, the base case of the recursion is in the
methods in the leaf nodes, the bottom-most nodes in the tree. All 
other nodes perform the recursive
case.  You can view the recursive computation as "walking" the tree,
systematically working its way down to the leaves and returning
values upwards. 

There are other ways to express tree structure.
In prefix notation, the expression tree above is 
"(Times (Plus 3 4) 5)". 
In Polish postfix 
notation it is "3 4 Plus 5 Times".  Trees can also be represented as 
lists, with indentation level to show hiearchy.  The same tree could 
be represented as 
- Times
  - Plus
    - 3
    - 4
  - 5

### ```eval``` is recursive

I hope you like recursion, because we've got more.  The ```__str__``` and 
```__repr__``` methods made recursive calls using the left and right 
operands.  So does ```eval```:

```python
    def eval(self) -> "IntConst":
        """Implementations of eval should return an integer constant."""
        left_val = self.left.eval()
        right_val = self.right.eval()
        return IntConst(left_val.value + right_val.value)
```

We'll reorganize evaluation a bit below, but for now 
we should be able to pass the test cases we wrote for 
evaluation of expressions constructed from ```Plus```
and ```IntConst```. 

### Checkpoint

At this point you have the base class `Expr` and two concrete 
subclasses, `IntConst` and `Plus`.  This is enough to represent
expressions that involve only addition, like 
`Plus(Plus(IntConst(5), IntConst(3)), IntConst(4))`.  In addition to 
passing the test cases in `test_expr.py`, you can check the 
functionality in the Python console: 

```pycon
>>> from expr import *

>>> Plus(Plus(IntConst(5), IntConst(3)), IntConst(4)).eval()
IntConst(12)
```

### Question (answer in questions.md)

How do we know that the `eval` method above will not loop forever? 

## Parsing input (first cut)

We could go on building up the ```expr.py``` module and 
test cases, but it would be more satisfying and reassuring
to see even a little bit of real calculator behavior. 
So, let's take a little detour and build a module to 
read input and build an ```Expr``` object (really a tree 
of ```Expr``` objects).  

Programming languges and related formal notations are
divided into at least three levels of descripton:
lexical, syntactic, and semantic.  The semantic
structure may be further divided into static and
dynamic semantics.

The lexical structure of a programming language is the way
an input text is divided into individual "tokens" or
"lexemes" like identifiers, operator symbols, and
numeric and string literals.   For example, if the input is
```(3 * 5)/x```, the lexemes should be
```["(", "3", "*", "5", ")", "/", "x" ]```.  Notice 
that white space is not included; the lexemes (or tokens)
are just the parts that make up the expression. 


 I have provided you a lexical analysis module, `lex.py`, to save
time and help you focus on the main issues in this 
 project. It provides a class `TokenStream` for obtaining each 
 lexeme (token), one by one.  Internally, `lex.py` uses 
 the *regular expression* package `re` to break the 
 input into tokens.  We will study regular expressions 
 later this term, but not yet. 
 
```python
class TokenStream(object):
    """
    Provides the tokens within a stream one-by-one.
    Example usage: 
       f = open("my_input_file")
       stream = TokenStream(f)
       while stream.has_more():
           token = stream.take()     # Removes token from front of stream
           lookahead = stream.peek() # Returns token without removing it
           # Do something with the token
    """
``` 

The ```TokenStream``` methods ```peek``` and ```take``` return
```Token``` objects, which hold both the text of the token and a 
classification. The ```Token``` class is very simple:

```python
class Token(object):
    """One token from the input stream"""

    def __init__(self, value: any, kind: TokenCat):
        self.value = value
        self.kind = kind

    def __repr__(self) -> str:
        return "Token({}: {})".format(repr(self.value), self.kind)

    def __str__(self) -> str:
        return repr(self)
```

The token categories are defined by an *enumeration*, which is a 
special kind of Python class that differs from normal classes. 
The enumeration we use for the lexical analysis is a bit tricky, 
but all we really need to know is that each category has a name. 
For example, if the integer 24 appears in the input, it will be 
represented as ```Token('24', TokenCat.INT)```, and the symbol 
'+' will be represented as ```Token('+', TokenCat.PLUS)```.  

### Reverse Polish Notation

While `lex.py` provides you with a stream of tokens 
(lexemes), we still need a way to combine these to 
build an `Expr`.  `rpncalc.py` is starter code for 
doing that. 

Eventually we would like to be able to parse and interpret an
expression in algebraic notation like ```(3*4)/6```,  and we 
*will* do that, but initially we want to keep it as simple 
as possible.  We can build a very, very simple parser using 
*reverse Polish notation*, or RPN. 

In RPN, an operator like '+' is written after its operands.  
Instead of ```3+4```, we write ```3 4 +```.  We can write 
```(3*4)/6``` as ```3 4 * 6 /```.  We can write
```3*(4/6)``` as ```3 4 6 / *```. 
Notice that we don't need parentheses! 

An RPN parser uses a stack structure.  An operand is "pushed" 
onto the stack. An operator like ```+``` or ```*``` pops two 
elements from the stack, and pushes the result.   In Python, 
a list can be used as a stack, using ```append``` as the push 
operation and ```pop``` as the pop method.  (That's why it's 
called ```pop```.)

Let's consider what the sequence should be for ````6 5 + 4 +```. 
Initially the stack is empty. 

![The stack is empty. "6 5 + 4 +" are waiting in the token stream
](img/RPN-calc-1.png
"Initial parse state")

We process the first token (6) and push a corresponding ```IntConst```
object

![The stack has one element, IntConst(6).  "5 + 4 +" are waiting
in the token streem
](img/RPN-calc-2.png
"After pushing an IntConst")

We likewise push the next value.

![The stack has two items, IntConst(5) on top and IntConst(6) below it.
"+ 4 +" are waiting in the token stream.
](img/RPN-calc-3.png "After pushing 6 and 5")

The next token is '+'.  We want to create a ```Plus``` node for it.  Where 
are the left and right operands?  On the stack.  We pop them, build the ```Plus```
object, and push it onto the stack. 

![On the stack is one item, a Plus node, but it has arrows
to the IntConst(5) and IntConst(6) nodes, which are no longer
on the stack.
](img/RPN-calc-4.png "Plus")

(Here `Plus` is the root of a tree 
that we will draw sideways so that we can 
draw the stack vertically.) 

Next from the token stream we have another integer, 4.
We push it onto the stack just as 
we did with the others. 

![The top element in the stack is IntConst(4).  Below it
is the Plus node with its pointers to the two IntConst nodes.
](img/RPN-calc-5.png "Another integer")

Finally we have another '+'.  We treat it exactly like the 
first: Pop the two operands, build the ```Plus``` object, 
and push it.  The only difference is that this time the 
left operand will be another ```Plus``` node. 

![Now the stack holds just one item, a "Plus" node.
This Plus node has arrows to IntConst(4), and to the other
Plus node, which in turn has arrows to IntConst(5) and IntConst(6)
](img/RPN-calc-6.png "Second Plus")

At the conclusion of this, if the input was 
syntactically correct, the top element of the stack 
holds the ```Expr``` object that represents the 
whole expression. 

At this point the only ```Expr``` classes we have are 
```IntConst``` and ```Plus```, so we can't build very 
interesting expressions, but it's nice to 
run `rpncalc.py` and see that it
is working as intended so far: 

```python
$ python3 rpncalc.py
Expression (return to quit):6 5 4 + +
(6 + (5 + 4)) => 15
Expression (return to quit):6 5 + 4 +
((6 + 5) + 4) => 15
Expression (return to quit):
```
#### Question to answer in questions.md

The constructor for a `Plus` node says that it takes two `Expr` nodes
as arguments,
but we are passing it `IntConst` and `Plus` nodes.  Is this ok?
Why or why not? 

## Back to Expr

Now we have a way of building ```Expr``` objects and 
evaluating them, but our only operation is ```Plus```.  
Let's add ```Times```.  It might look like this: 

```python
class Times(Expr):
    """left * right"""

    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def eval(self) -> "IntConst":
        """Implementations of eval should return an integer constant."""
        left_val = self.left.eval()
        right_val = self.right.eval()
        return IntConst(left_val.value * right_val.value)

    def __str__(self) -> str:
        """Implementations of __str__ should return the expression in algebraic notation"""
        return f"({str(self.left)} * {str(self.right)})"

    def __repr__(self) -> str:
        """Implementations of __repr__ should return a string that looks like
        the constructor, e.g., Plus(IntConst(5), IntConst(4))
        """
        return f"Times({repr(self.left)}, {repr(self.right)})"
```

Should we happy about this?  It works.  It was fairly easy copying code 
from the ```Plus``` class and making a few changes.  But we
are not happy. Repeating code that is almost the same is not good.
It gives us too many chances to make errors, particularly some time
in the future when we change some of that code but fail to
change it everywhere consistently.  

![Frowny face](img/unhappy.png 
"Frowny face with caption 'Actual photograph of programmer reading 
repetitive code")

## DRY it out! 

Recalling the slogan "Don't Repeat Yourself" (DRY), we want to find a way 
to "factor out" what is common between ```Plus``` and ```Times``` (and other
arithmetic operators we haven't written yet).  We would like to create an 
abstract superclass that contains the common code, and as far as possible 
just write code specific to each operation in the class for that operation. 

We'll start by creating class ```BinOp``` (arithmetic operations with 
two operands) and see what we can *factor* into it. 

```python
class BinOp(Expr):
    pass

class Plus(BinOp):
    """left + right"""
    # ... as before
    
class Times(BinOp):
    """left * right"""
    # ... as before
```

PyCharm may complain that our new ```BinOp``` class does not implement
all the methods of ```Expr```.  That's ok, because ```BinOp``` itself
is abstract. That is, we're not going to create objects of class
```BinOp```; we'll only create objects of classes ```Plus```,
```Times```, etc.  (There is a way in Python to mark the class as
abstract and suppress the warnings from PyCharm and other tools,
but it is unwieldy.  I don't want to deal with it here.)

```eval``` is going to be the most interesting method to factor out, 
but let's start simpler with ```__str__```.  The only difference between
the string representation of ```Plus``` and the string representation of 
```Times``` is the symbol, '+' for ```Plus``` and '*' for ```Times```. 

![Side-by-side code of Times and Plus, as explained below](
img/binop-refactor.png
"Differences between string methods in Plus and Times")

The constructor is the same (setting the `left` and `right` 
instance variables) and the `__str__` and `__repr__` methods 
differ only in the operation symbol ("+" or "*") and the 
class name ("Plus" or "Times").  We could factor out all of this 
common code into the `BinOp` class if we just put the operation 
symbol and class name in variables.  Let's factor all the initialization
except for the choice of symbol into the constructor for `BinOp`:


```python
class BinOp(Expr):
    """Abstract base class for binary operations"""
    def __init__(self, left: Expr, right: Expr, symbol: str="?Operation symbol undefined"):
        self.left = left
        self.right = right
        self.symbol = symbol
```
Now the constructors of concrete subclasses can delegate to the
constructor of `BinOp`, providing the appropriate symbol: 

```python
class Plus(BinOp):
    """Expr + Expr"""
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="+")
```

We've saved a few lines of repetitive code.  A bigger gain 
comes from factoring the `__str__` and `__repr__` methods into
`BinOp` and removing them from `Plus`.  The `__str__` class
in `BinOp` can be: 

```python
    def __str__(self) -> str:
        return f"({self.left} {self.symbol} {self.right})"
```

Now the `__str__` method can be removed from the `Plus` class. 

Factoring the `__repr__` method is slightly more complex.  Recall 
how we obtained the name of a class in abstract methods in class `Expr`
as `self.__class__.__name__`.  We can use that to build a generic 
`__repr__` method in class `BinOp`: 

```python
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}({repr(self.left)}, {repr(self.right)})"
```

Now our concrete classes for binary operators can inherit
the `__repr__` method from `BinOp` rather than each providing
their own.   We can similarly factor out the `__str__` methods
by passing the operator symbol from the constructor of
a concrete class for a binary operator to the abstract
`BinOp` class, like this: 

```python
class Plus(BinOp):
    """Represents left + right"""
    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, symbol="+")
```

Our concrete classes for classes like `Plus` and `Minus`
are getting smaller and simpler! 

### Checkpoint

We have not added any new functionality in this step, but we have 
simplified the code.  Now you have classes `Expr`, `BinOp`, `Plus`, 
and `Times`.  The only methods in `Plus` and `Times` are the 
constructor (`__init__`), which calls its superclass with
one extra argument for the operation symbol, and `eval`.  It should 
still pass the 9 test cases we have written in `test_expr.py`. 

## Factoring evaluation

We can refactor even more.  

The only thing that differs in the ```eval``` methods of ```Plus```
and ```Times``` is that the former adds the left and right values 
and the latter multiplies them.  We can add an 
internal method ```_apply``` to each of the ```BinOp``` classes. 

We will need an abstract method `_apply` in the `BinOp` class: 

```python
    def _apply(self, left_val: int, right_val: int) -> int:
        """Each concrete BinOp subclass provides the appropriate method"""
        raise NotImplementedError(
            f"'_apply' not implemented in {self.__class__.__name__}\n"
            "Each concrete BinOp class must define '_apply'")
```

Then the  concrete subclasses like `Plus` can override it, for example

```python
    def _apply(self, left: int, right: int) -> int:
        return left + right
```

This is a good deal simpler than `eval`, which we can now factor 
into the `BinOp` class like this: 


```python
    def eval(self) -> "IntConst":
        """Each concrete subclass must define _apply(int, int)->int"""
        left_val = self.left.eval()
        right_val = self.right.eval()
        return IntConst(self._apply(left_val.value, right_val.value))
```

At this point our ```Plus``` and ```Times``` classes are short and clear.
Mine are just 5 lines of code each, not counting comments and blank lines.  
This is a good time to write a ```Div``` class and a ```Minus``` class. 
```Div``` should implement integer truncating division, ```//```
rather than ```/``` in Python.  It would be straightforward to add 
additional binary  operations like ```Remainder```, implemented by 
```%``` in Python. Adding a new binary operator in ```expr.py```
has become very simple.

#### Question to answer in questions.md

Method `_apply` returns an `int` rather than an `IntConst`.
How does the result of a binary operation become an
`IntConst` object? 

![Smiley face decoration](img/happy.png "Happy programmer")

We can add the following test cases in `test_expr.py` to increase our 
confidence that we have implemented all four operations correctly: 

```python
class TestBinOp(unittest.TestCase):
    """Test the remainder of the binary operations"""

    def test_div(self):
        exp = Div(IntConst(7), IntConst(3))
        self.assertEqual(exp.eval(), IntConst(2))

    def test_sub(self):
        exp = Minus(IntConst(7), IntConst(3))
        self.assertEqual(exp.eval(), IntConst(4))

    def test_composed(self):
        """Putting them all together: (10 - (2 + 1)) * (4 / 2) = 14"""
        exp = Times(
            Minus(IntConst(10), Plus(IntConst(2), IntConst(1))),
            Div(IntConst(4), IntConst(2)))
        self.assertEqual(exp.eval(), IntConst(14))
```

### Checkpoint

You should now have classes `Expr`, `Binop`, `Plus`, `Minus`, `Times`, 
and `Div`.  Classes `Plus`, `Minus`, `Times`, and `Div` are very 
similar and all very short.  They pass all 12 test cases. 

## Unary operations

Negation, which changes 42 to -42 and vice versa, is a unary operator. 
We might represent it in the RPN calculator language as ```~``` to 
avoid ambiguity.  
Absolute value is also a unary operation.  We customarily write the 
absolute value of *x* as ```|x|```, but for our RPN calculator it will 
be better if we have a single symbol.  We'll use ```@```.  

Add a new abstract base class ```Unop``` for unary operations, and add 
classes ```Abs``` and ```Neg``` to implement them.  Follow the same 
general approach as we did with ```BinOp```, except that ```Unop``` 
expressions have a ```left``` operand only. 

We can write and try a few more test cases before we enhance the 
RPN calculator to enable interactive checking of `Neg` and `Abs`. 

```python
class TestUnOp(unittest.TestCase):

    def test_repr_simple(self):
        exp = Abs(IntConst(5))
        self.assertEqual(repr(exp), "Abs(IntConst(5))")
        exp = Neg(IntConst(6))
        self.assertEqual(repr(exp), "Neg(IntConst(6))")

    def test_str_simple(self):
        exp = Abs(IntConst(12))
        self.assertEqual(str(exp), "(@ 12)")
        exp = Neg(IntConst(13))
        self.assertEqual(str(exp), "(~ 13)")

    def test_abs_eval(self):
        exp = Minus(IntConst(3), IntConst(5))
        self.assertEqual(exp.eval(), IntConst(-2))
        exp = Abs(exp)
        self.assertEqual(exp.eval(), IntConst(2))

    def test_neg_eval(self):
        exp = Minus(IntConst(12), IntConst(8))
        self.assertEqual(exp.eval(), IntConst(4))
        exp = Neg(exp)
        self.assertEqual(exp.eval(), IntConst(-4))

    def test_together(self):
        """Compose unary and """
        exp = Abs(Plus(IntConst(3), Neg(IntConst(12))))
        self.assertEqual(str(exp), "(@ (3 + (~ 12)))")
        self.assertEqual(exp.eval(), IntConst(9))
```

### Checkpoint

At this point, in addition to the `Expr` and all the `BinOp` classes,
you have `UnOp` and its concrete subclasses `Neg`, and `Abs`.  
There are now 17 test cases. 

#### Question to answer in questions.md

We noted above that an expression like `2+(5*3)` could
be expressed algebraically (this is also called "infix" notation),
in reverse Polish notation (also called "postfix"), or
in "prefix" notation like `+ 2 * 5 3`.  Which of these notations
have we adopted for the `__str__` methods of our `Expr` classes?

## Enhancing the RPN Calculator

To use our new operations interactively, we need to enhance the parser 
in ```rpncalc.py```.  As soon as we start to do so, we notice that 
once again we are producing very repetitive code: 

```python
            elif tok.kind == lex.TokenCat.PLUS:
                right = stack.pop()
                left = stack.pop()
                stack.append(expr.Plus(left, right))
            elif tok.kind == lex.TokenCat.TIMES:
                right = stack.pop()
                left = stack.pop()
                stack.append(expr.Times(left, right))
            elif tok.kind == lex.TokenCat.DIV:
                right = stack.pop()
                left = stack.pop()
                stack.append(expr.Div(left, right))
            elif tok.kind == lex.TokenCat.MINUS:
                right = stack.pop()
                left = stack.pop()
                stack.append(expr.Minus(left, right))
```

It would be much too easy to make a small mistake in one of those 
cases and never see it!  What can we do? 


### Moving logic to tables

 
So far we've used multiple tactics to factor repetitive code. 
For `__str__`  in `BinOp` and `UnOp`, we were 
able to factor out differences to a variable.  For `eval` we 
were able to factor out differences to the small method `_apply`
that could be inherited from an abstract base class, `BinOp` or `UnOp`. 
Unfortunately we can't use quite the same tactic 
for the repetitive code in the RPN calculator, because 
it isn't replicated 
from class to class (although it refers to classes). 
 The code is 
repeated within branches of a single function. We'll need another 
tactic. 

Often we can simplify code like this with 
a table.  Again the question we ask is "what is being repeated, 
and what is the variation?"   We want to write the repeated code 
once, and keep the variations in the table. 

Each of the branches for a binary operator associates a lexical 
token category with a subclass of `BinOp`.  Let's put that 
association in a table, in the form of a Python dictionary: 

```python
BINOPS = { lex.TokenCat.PLUS : expr.Plus,
           lex.TokenCat.TIMES: expr.Times,
           lex.TokenCat.DIV: expr.Div,
           lex.TokenCat.MINUS:  expr.Minus
        }
```

Now elif/elif/elif code above can be compressed to a 
single branch: 

```python
            elif tok.kind in BINOPS:
                binop_class = BINOPS[tok.kind]
                right = stack.pop()
                left = stack.pop()
                stack.append(binop_class(left, right))
```

We can do the same thing with unary operators.  I have already 
 added them to ```TokenCat``` in ```lex.py```: 

```python
class TokenCat(Enum):
    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIV = r"/"
    NEG = r"~"
    ABS = r"@"
    LPAREN = r"\("
    RPAREN = r"\)"
    INT = r"[0-9]+"
    ignore = r"\s+|#.*"   # Whitespace and comments
    error = "."           # catch-all for errors
    END = "###SHOULD NOT MATCH###"  # Not really a pattern
```


Where are my test cases?  I'll write a more systematic set of test cases 
soon, but all along I've been doing quick smoke tests by running the 
RPN calculator.  For example: 

```python
Expression (return to quit): 5 3 * 4 /
((5 * 3) / 4) => 3
Expression (return to quit):3 7 + 4 - 
((3 + 7) - 4) => 6
Expression (return to quit):
```

Add the unary operators, with a similar table.  Then 
we'll be able to check our operators interactively 
in the calculator: 

```
Expression (return to quit):3 5 - @
@ (3 - 5) => 2
Expression (return to quit):3 5 -
(3 - 5) => -2
Expression (return to quit):
Bye! Thanks for the math!
```

## Test cases for expressions

Initially I wrote a set of test cases for ```Plus```. I could 
write a similar set for every each concrete subclass of ```Expr```. 
However, now that I've made it very easy to add new 
binary and unary operators, I would like to make it easier
to write new test cases.  

At present the `calc` function in `rpncalc.py` 
parses a line and then executes it, printing a result. 
I can't easily use the `calc` function in a test 
case, because it prints its result instead of returning 
a value.  So, to make testing easier, I will factor 
out the expression parsing part of `calc`.   Most of the
original `calc` will be copied into a new function `rpn_parse`.
The new `calc` will be cut down to: 

```python
def calc(text: str):
    """Read and evaluate a single line formula."""
    try:
        stack = rpn_parse(text)
        if len(stack) == 0:
            print("(No expression)")
        else:
            # For a balanced expression there will be one Expr object
            # on the stack, but if there are more we'll just print
            # each of them
            for exp in stack:
                print(f"{exp} => {exp.eval()}")
    except Exception as e: 
        print(e)
```

The `calc` function prints exceptions but does not re-raise them, 
so that the main function can loop through correct and incorrect 
inputs. `calc` will call `rpn_parse`: 

```python
def rpn_parse(text: str) -> list[expr.Expr]:
    """Parse text in reverse Polish notation
    into a list of expressions (exactly one if
    the expression is balanced).
    Example:
        rpn_parse("5 3 + 4 * 7")
          => [ Times(Plus(IntConst(5), IntConst(3)), IntConst(4)))),
               IntConst(7) ]
    May raise:  ValueError for lexical or syntactic error in input 
    """
```

I leave most of the body of `rpn_parse` to you.  Note that there are 
two distinct exceptions that the RPN parser could encounter a 
`LexicalError` exception from the lexer, or an `IndexError` if the 
expression is unbalanced.  The `LexicalError` is descriptive enough, 
so we can just pass it on: 

```python
    except lex.LexicalError as e:
        # Lexer choked on input; re-raise the exception with its original message
        raise
```

`IndexError`, on the other hand, is not a good explanation of what 
was wrong with an input expression.  We'll translate it to a 
`ValueError` with a descriptive message: 

```python
    except IndexError:
        # Stack underflow means the expression was imbalanced
        raise ValueError(
            f"Imbalanced RPN expression, missing operand at {tok.value}")
```


Whereas the ```calc``` function was not useful in our test 
suite, the ```rpn_parse``` function is useful.  I put the following
in a separate test module, `test_rpncalc.py`: 

```python
class TestParseRPN(unittest.TestCase):

    def test_parse_add(self):
        exp = rpn_parse("5 4 +")[0]
        self.assertEqual(str(exp), "(5 + 4)")
        self.assertEqual(repr(exp), "Plus(IntConst(5), IntConst(4))")
        self.assertEqual(exp.eval(), IntConst(9))
        
    def test_parse_times(self):
        exp = rpn_parse("5 3 * ")[0]
        self.assertEqual(repr(exp), "Times(IntConst(5), IntConst(3))")
        self.assertEqual(str(exp), "(5 * 3)")
        self.assertEqual(exp.eval(), IntConst(15))
        
    def test_parse_minus(self):
        exp = rpn_parse("5 3 -")[0]
        self.assertEqual(str(exp), "(5 - 3)")
        self.assertEqual(repr(exp), "Minus(IntConst(5), IntConst(3))")
        self.assertEqual(exp.eval(), IntConst(2))
        
    def test_parse_div(self):
        exp = rpn_parse("7 3 /")[0]
        self.assertEqual(str(exp), "(7 / 3)")
        self.assertEqual(repr(exp), "Div(IntConst(7), IntConst(3))")
        self.assertEqual(exp.eval(), IntConst(2))
        exp = rpn_parse("3 7 /")[0]
        self.assertEqual(exp.eval(), IntConst(0))
```

It's still a little tedious, and I made several typos when I first 
wrote the test case, but it's more compact than it would 
otherwise be.  Where ```rpn_parse``` really saves effort is in 
testing a more complex expression: 

```python
    def test_a_bigger_expr(self):
        exps = rpn_parse("60 2 / 30 10 - + 2 *")
        self.assertEqual(len(exps), 1)
        exp = exps[0]
        self.assertEqual(exp.eval(), IntConst(100))
```

Also at this point we can perform larger calculations 
interactively: 

``` 
$ python3 rpncalc.py 
Expression (return to quit):3 7 - 14 * 2 / ~
~ (((3 - 7) * 14) / 2) => 28
Expression (return to quit):
```

### Checkpoint

In addition to all the `BinOp` and `UnOp` classes in `expr.py`,
you now have `rpn_parse`, `calc`, and `rpn_calc` in `rpncalc.py`.
A separate test file `test_rpncalc.py` has five test cases, in 
addition to those in `test_expr.py`.

#### Question to answer in questions.md

Our postfix notation uses "~" for negation and reserves
"-" for subtraction.  Why? Can you give an example 
postfix (reverse Polish notation) expression that
would be ambiguous if we used "-" as both a 
unary and binary operation? 

## Adding variables

That's all very nice, but a modern calculator should 
have a memory ... maybe just a handful of variables, 
but we should be able to calculate a value from a 
formula once and then use it several times.  Sticking with 
RPN, I might write 

```
24 60 * 60 * seconds_per_day =
30 seconds_per_day *
```

We'll keep these variables in an object we'll call 
an *environment*.   We could create a new class, but a 
Python dict should do nicely.  We'll also need to 
create a class for a variable.   Evaluating a variable
will look up its value in the environment.  Assigning to 
a variable will store a value in the environment.  

A key design decision is whether there is just one, 
global environment, or the possibility of several 
different environments.  If there is only one environment, 
we can make it a global variable in the ```expr``` module 
(the ```expr.py``` file), but then all ```Expr``` objects 
share it.  If we wanted to expand our calculator into a 
full programming language interpreter, this would not be 
satisfactory.  Our programming language would likely have 
*scopes*, like Python and other programming languages.  To 
support multiple scopes, we would need to make the current 
environment an additional argument to ```eval```.

For this project we'll take the easy way out:  There is just one 
global environment, in the ```expr``` module scope.  Near the 
beginning of ```expr.py``` we can add: 

```python
# One global environment (scope) for 
# the calculator

ENV: dict[str, "IntConst"] = dict()
```

I use all-caps for ```ENV``` as a reminder that it is a global variable.
The type annotation must place `IntConst` in quotes because the 
`IntConst` class is defined later in the file. 

Calculators usually have an "all-clear" button to clear all memory.  We 
might consider writing a corresponding function this way: 

```python
def env_clear():
    """Clear all variables in calculator memory"""
    ENV = dict()
```

But this will not work!  It will create a variable ```ENV``` in the local 
scope of the function ```env_clear```, rather than changing the global 
variable ```ENV```.  We need to specify that the ```ENV``` variable
we mean is the global ```ENV```:

```python
def env_clear():
    """Clear all variables in calculator memory"""
    global ENV
    ENV = dict()
```

I have not added an "all clear" command to the calculator interface;
you may want to try it after completing the project. 

Now we can make an ```Expr``` subclass ```Var```.  Its 
```eval``` method will look in the environment for a value, 
which should be an ```IntConst```.  What if a variable by 
that name is not found?  We could give it a default value, 
or we could raise an exception.  Our RPN calculator is already 
catching exceptions for lexical and syntax errors, so it is 
easy enough to add one for reference to a variable that 
doesn't have a value.  We'll add: 

```python
class UndefinedVariable(Exception):
    """Raised when expression tries to use a variable that 
    is not in ENV
    """
    pass
```

We can get started on the ```Var``` class:   

```python
class Var(Expr):

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var({self.name})"

    def eval(self):
        global ENV
        if self.name in ENV:
            return ENV[self.name]
        else:
            raise UndefinedVariable(f"{self.name} has not been assigned a value")
```

What about assigning a value to a variable?  The method in the 
```Var``` class is not hard: 

```python
    def assign(self, value: IntConst):
        # You fill this in
```

But how should we represent assignment in the calculator input 
and the ```Expr``` structure?  We'd like the RPN input to look like 

```
3 5 + x =
```

to assign value 8 to variable x.  But what about this? 

```
8 x = 5 +
```

Should this be an error, or should it return 13?   The ```eval``` method 
in all of our other ```Expr``` classes returns an ```IntConst```.  For 
consistency, and to avoid special cases in our calculator logic, we 
will make an ```Assign``` class with an ```eval``` that sets a 
variable value *and* also returns a value. 

The 'left' operand of an ```Assign``` object must always 
be a ```Var```: 

```python
class Assign(Expr):
    """Assignment:  x = E represented as Assign(x, E)"""
    
    def __init__(self, left: Var, right: Expr):
        assert isinstance(left, Var)  # Can only assign to variables! 
        self.left = left
        self.right = right
```

Note the `Assign` class is not the same as the `assign` method of 
`Var`.   The `Assign` class will use `Var.assign` in its `eval` method. 
The ```eval``` method of ```Assign``` evaluates its right side but
not its left side:

```python
    def eval(self) -> IntConst: 
        r_val = self.right.eval()
        self.left.assign(r_val)
        return r_val
``` 

I leave the ```__str__``` and ```__repr__``` methods to you. 

When we have a working `Var` class and `Assign` class, 
the following test case in `text_expr.py` should pass: 

```python
class TestVars(unittest.TestCase):
    def test_assign(self):
        v = Var("v")
        w = Var("w")
        exp = Assign(v, IntConst(5))
        self.assertEqual(exp.eval(), IntConst(5))
        self.assertEqual(v.eval(), IntConst(5))
        exp = Assign(w, v)
        self.assertEqual(exp.eval(), IntConst(5))
        self.assertEqual(w.eval(), IntConst(5))

    def test_assign_reps(self):
        v = Var("v")
        w = Var("w")
        exp = Assign(v, Plus(IntConst(5), w))
        self.assertEqual(str(exp), "(v = (5 + w))")
        self.assertEqual(repr(exp), "Assign(Var(v), Plus(IntConst(5), Var(w)))")
```


At this point our `text_expr.py` contains 19 test case methods. 

To parse assignments, I need to add cases in ```rpn_calc``` for 
variables and assignments.  Variables are straightforward, 
and I leave them to you. 

For assignments, I want to do something slightly different. 
In programming languages we typically put the variable 
on the left side of the assignment statement, like 
```x = 3 + 4```, and I've used that convention in making 
the variable be the ```left``` field of an ```Assign``` object. 
However, in RPN I find it difficult to read 

```
x 3 4 + 5 * 7 / =
```

A long expression separates the variable from the ```=``` symbol. 
I prefer 

```
3 4 + 5 * 7 / x =
```

So I want to swap "left" and "right" between algebraic notation
(as produced by the ```__str__``` method) and RPN notation.  I 
do this by swapping left and right in the constructor call: 

```python
        elif tok.kind == lex.TokenCat.ASSIGN:
            right = stack.pop()
            left = stack.pop()
            # Reverse left and right 
            stack.append(expr.Assign(right, left))
```

With this in place, I can now make calculations involving variables: 

```
Expression (return to quit): 24 60 * 60 * seconds_per_day =
(seconds_per_day = ((24 * 60) * 60)) => 86400
Expression (return to quit):7 seconds_per_day * seconds_per_week =
(seconds_per_week = (7 * seconds_per_day)) => 604800
Expression (return to quit):seconds_per_week
seconds_per_week => 604800
Expression (return to quit):
```

We should also add a test case
that uses `rpn_parse` to `test_rpncalc.py`:

```python
class TestRPNAssignment(unittest.TestCase):

    def test_env_global(self):
        exp = rpn_parse("5 4 3 * + x =")[0]
        self.assertEqual(str(exp), "(x = (5 + (4 * 3)))")
        self.assertEqual(exp.eval(), IntConst(17))
        exp = rpn_parse("x 3 +")[0]
        self.assertEqual(exp.eval(), IntConst(20))
```

## Are we done yet? 

At this point we have a full working RPN calculator. 
The `rpn_parse` function in `rpncalc.py` contains cases for
integer constants, binary operations, unary operations,
variables, and assignments.  Our `Expr` subclasses include
`IntConst`, `Var`, and `Assign`, as well as
subclasses `Plus`, `Times`, `Minus`, and `Div` of `BinOp` and
subclasses `Neg` and `Abs` of `UnOp`. 

It is ready to turn in.   You will turn in `expr.py` and
`rpncalc.py`.  You will not turn in the test suites. 

#### Question to answer in questions.md

Suppose we wanted to add exponentiation to our calculator, so
that the RPN expression `5 2 ^` would evaluate to 25 (5 squared)
and `5 3 ^` would evaluate to 125 (5 cubed).  Assume the lexer
returns a token `lex.TokenPat.POWER`.  What new class would I
need to add to `expr.py`, and what would it be a subclass of? 
What change would I need to make to `rpncalc.py`?


## Bonus: An algebraic calculator

I'd like to also 
create a calculator that takes algebraic notation. 
The internal representation of expressions can be exactly 
the same.  All that is different is the 
way the input is parsed.  And so, if your 
```rpncalc.py``` is working correctly, you should 
find that ```llcalc.py``` also works: 

```
Expression (return to quit):lec = 80 # Minutes per lecture
lec = 80 => 80
Expression (return to quit):weeks = 10
weeks = 10 => 10
Expression (return to quit):lecs_week = 2
lecs_week = 2 => 2
Expression (return to quit):midterms = 1 
midterms = 1 => 1
Expression (return to quit):total_lec = (weeks * lecs_week - midterms) * lec
total_lec = (((weeks * lecs_week) - midterms) * lec) => 1520
Expression (return to quit):
Bye! Thanks for the math!
```

This document is long enough, but I explain 
how the algebraic calculator works in a 
separate document, ```LLPARSING.md```. 
You do not have to read it, 
but you may find it interesting. 
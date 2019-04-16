# Parsing

"Parsing" means analyzing a linear stream of symbols to 
recognize its hierarchical structure.  Reverse Polish
notation is a particularly simple kind of linear stream 
of symbols.  We can analyze its hieararchical structure 
(and perhaps represent it as a tree, as in the Expr structure)
using a stack and simple rules for pushing and popping. 

Parsing programming languages and algebraic notation like 
x + y * z is a little more complicated, but not completely 
mysterious.  You can get the in-depth version and learn to 
write compilers and interpreters by taking CIS 461 in a couple
years.  

You do *NOT* need to modify the ```llcalc.py``` file or
understand it for this project.  You can stop reading this 
document right now if you're not interested.  But you might 
be interested, so I'm going to try to give you a brief
explanation of how it works. 

## Grammar

The syntactic structure of a language is described by a grammar. 
A grammar is usually specified by a set of rules that look 
something like this: 

```
sentence ::=  subject verb object
sentence ::= subject verb
subject ::= noun_phrase
object ::= noun_phrase
```
Read this as "A sentence can be a subject, followed by a verb, followed 
by an object, or a sentence can be a subject followed by a verb.  A subject 
can be a noun_phrase.  An object can be a noun_phrase."   Grammars can 
be used to describe both human languages and programming languages. 
Human languages are far too complex to describe completely in this manner. 
Programming languages are much simpler. We can (almost) completely describe
their syntactic structure by such rules. 

The grammar for our calculator language might look like this: 

```
expression ::= VAR = expression
expression ::= expression * expression
expression ::= expression + expression
expression ::= expression / expression
expression ::= expression - expression
expression ::= VAR
expression ::= INT
expression ::= ( expression ) 
```
This grammar describes all the inputs that the algebraic version 
of our calculator accepts, but there's a problem:  It's very ambiguous. 
For example, "5-3-2" could be parsed as (5-3)-2 or as 5-(3-2).  

A grammar that is useful for parsing must be unambiguous.  There must be, 
for example, only one way for "5-3-2" to be accounted for in the grammar. 
Moreover, we want to be able to parse fairly quickly (in linear time), 
without trying all possible ways of matching the input to the grammar.  Often 
we construct grammars with more restricted rules to make parsing fast and 
convenient. 

## Recursive descent

One of the common approaches to parsing is *recursive descent*.  
The basic idea is that the parsing functions directly mirror the 
grammar.  If we have a grammar rule like 
```
expression ::= term '+' expression
```
then there will be a function *expression* that attempts to match 
a *term*  (by calling the function that matches the *term* pattern), 
then the symbol "+", and then (recursively!) another *expression*.  
When there is more than one grammar rule for a particular symbol, 
like expression, we must have a way of predicting which rule to use, 
usually by looking at just one symbol in the input.  

```llcalc.py``` uses recursive descent parsing.  (It is called llcalc
because the form of grammar that we can parse with recursive descent, 
choosing grammar rules by looking just at the next symbol in the input, 
is called LL(1).)  There is a grammar given in ```llparse.py```: 

```python
#  program ::= stmt
#  stmt ::= exp ['=' exp]
#  exp ::= term { ('+'|'-') term }
#  term ::= primary { ('*'|'/')  primary }
#  primary ::= IDENT | CONST | '(' exp ')'
```

This grammar is only documentation.  The functions ```_stmt```, ```_exp```, 
etc. were written to follow the grammar.  (In fact I first designed the 
grammar, then cranked out the corresponding code while reading the grammar.)
This grammar uses a few shorthand features that make it more compact. 
The symbol "|" means "or", so 

```
#  primary ::= IDENT | CONST | '(' exp ')'
```

means that a *primary* can be an identifier, an integer constant, or 
a parenthesized expression (and the function ```_primary``` will have 
to predict which of those alternatives to match by looking at a 
single symbol).  [ and ] enclose an optional item, and { and } enclose 
an item that may be repeated zero or more times.  

Notice that the precedence of arithmetic operations is captured by a hierarchy
of grammar symbols: 

```
#  exp ::= term { ('+'|'-') term }
#  term ::= primary { ('*'|'/')  primary }
#  primary ::= IDENT | CONST | '(' exp ')'
```

Unless you are already very familiar with parsing and grammars, it will 
not be obvious that these rules say multiplication and division are 
higher precedence than addition and subtraction, and that parentheses can 
be used to group terms that should be evaluated first.  
But that is what they say.   

While I expect parsing is new to you, and I certainly wouldn't ask you to 
write a recursive descent parser yet, you may find that with this little bit of background
the code in ```llcalc.py``` is not so mysterious. 

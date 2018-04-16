"""
Driver (main program) for symbolic calculator.
"""

from rpn_parse import parse, InputError
from lexer import LexicalError
import expr
import calc_state

HELP_MSG = """Type 'quit' to quit.
Assignment: 'expression var ='
Form expressions with +, -, *, /, ~ (negation)
Use a space between each element, e.g.,
for y_not gets z + 3:
  yes:  y_not z 3 + =
   no:  y_not z3+=
Identifiers can be any_valid_P7thon_identifier
"""


def main():
    """Evaluate expressions typed at the command line"""
    env = calc_state.Env(expr.Const, expr.Const(0))
    while True:
        try:
            inp = input("expression/'help'/'quit': ")
            if inp == "quit":
                break
            elif inp == "dump":
                print(str(env))
            elif inp == "clear":
                env.clear()
            elif inp in ["help", "?", "Help"]:
                print(HELP_MSG)
            else:
                exp = parse(inp)
                print("({}) -> ".format(exp), end='')
                print(exp.eval(env))
        except InputError as e:
            print(e)
            print(HELP_MSG)
        except LexicalError as e:
            print(e)
            print(HELP_MSG)
        except NotImplementedError as e:
            print(e)


if __name__ == "__main__":
    main()

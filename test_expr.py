"""
Tests for expr.py, 
  (excludes parsing)

"""

import unittest
import expr
import calc_state


class TestExpr(unittest.TestCase):

    def test_const(self):
        env = calc_state.Env(expr.Const, expr.Const(0))
        seven = expr.Const(7)
        self.assertEqual('Const(7)', repr(seven))
        self.assertEqual('7', str(seven))
        self.assertEqual(seven.eval(env), expr.Const(7))

    def test_plus(self):
        env = calc_state.Env(expr.Const, expr.Const(0))
        eight = expr.Const(8)
        nine = expr.Const(9)
        x = expr.Var('x')
        y = expr.Var('y')
        self.assertEqual(expr.Plus(x, y), expr.Plus(x, y))
        self.assertEqual(expr.Plus(eight, nine).eval(env), expr.Const(17))
        self.assertEqual(expr.Plus(eight, expr.Plus(nine, eight)).eval(env),
                         expr.Const(25))
        self.assertEqual("Plus(Const(8), Const(9))", repr(expr.Plus(eight, nine)))
        self.assertEqual("(8 + 9)", str(expr.Plus(eight, nine)))

    def test_minus(self):
        env = calc_state.Env(expr.Const, expr.Const(0))
        eight = expr.Const(8)
        nine = expr.Const(9)
        x = expr.Var('x')
        y = expr.Var('y')
        self.assertEqual(expr.Minus(x, y), expr.Minus(x, y))
        self.assertEqual(expr.Minus(nine, eight).eval(env), expr.Const(1))
        self.assertEqual(expr.Minus(eight, expr.Minus(nine, eight)).eval(env),
                         expr.Const(7))
        self.assertEqual("Minus(Const(8), Const(9))", repr(expr.Minus(eight, nine)))
        self.assertEqual("(8 - 9)", str(expr.Minus(eight, nine)))

    def test_times(self):
        env = calc_state.Env(expr.Const, expr.Const(0))
        three = expr.Const(3)
        four = expr.Const(4)
        x = expr.Var('x')
        y = expr.Var('y')
        self.assertEqual(expr.Times(x, y), expr.Times(x, y))
        self.assertNotEqual(expr.Times(x, y), expr.Plus(x, y))
        self.assertEqual(expr.Times(three, four).eval(env), expr.Const(12))
        self.assertEqual(expr.Times(three, expr.Times(three, four)).eval(env),
                         expr.Const(36))

    def test_div(self):
        env = calc_state.Env(expr.Const, expr.Const(0))
        three = expr.Const(3)
        nine = expr.Const(9)
        x = expr.Var('x')
        y = expr.Var('y')
        self.assertEqual(expr.Div(x, y), expr.Div(x, y))
        self.assertNotEqual(expr.Div(x, y), expr.Times(x, y))
        self.assertEqual(expr.Div(nine, three).eval(env), expr.Const(3))
        self.assertEqual(expr.Div(nine, expr.Times(three, three)).eval(env),
                         expr.Const(1))

    def test_assign(self):
        """Assignments:  Assign(var, exp) """
        env = calc_state.Env(expr.Const, expr.Const(0))
        x = expr.Var('x')
        y = expr.Var('y')
        # Treat variables as having initial value zero
        self.assertEqual(y.eval(env), expr.Const(0))
        self.assertEqual(x.eval(env), expr.Const(0))
        expr.Assign(expr.Const(5), x).eval(env)
        # x changed but y unchanged
        self.assertEqual(y.eval(env), expr.Const(0))
        self.assertEqual(x.eval(env), expr.Const(5))
        # We can use x and y in an expression
        result = expr.Plus(expr.Times(x, expr.Const(3)), y).eval(env)
        self.assertEqual(result, expr.Const(15))


if __name__ == '__main__':
    unittest.main()

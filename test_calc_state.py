"""
Unit tests for calc_state.py
"""

import unittest
import calc_state

class TestStore(unittest.TestCase):

    def test_basic(self):
        env = calc_state.Env[str](str, "No value")
        self.assertEqual(env.get("A"), "No value")
        env.put("A", "some value")
        self.assertEqual(env.get("A"), "some value")
        env.put("A", "another value")
        self.assertEqual(env.get("A"), "another value")
        env.put("B", "a third value")
        self.assertEqual(env.get("A"), "another value")        
        self.assertEqual(env.get("B"), "a third value")
        env.clear()
        self.assertEqual(env.get("A"),  "No value")
        self.assertEqual(env.get("B"), "No value")

    def test_bad_type(self):
        env = calc_state.Env[str](str, "No value")
        with self.assertRaises(AssertionError):
            env.put("A", 42)
        

if __name__ == '__main__':
    unittest.main()
    

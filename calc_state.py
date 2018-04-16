"""
Calculator state.  Expressions are evaluated in the
context of a memory state (Env), which is a relation between
variable names and values.  Values are 'opaque' to to 
the store:  We do not import 'expr' here, even though 
we might be storing values of type 'Expr'.  As a 
debugging aid, we do support specifying the expected 
value type, and checking that only that value type is 
stored. This way expr.py depends on calc_state.py, but 
not vice versa.  

"""

from typing import TypeVar, Generic, Type

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

# Whatever value type we will store in this
# environment ... 
Value: TypeVar = TypeVar('Value')


class Env(Generic[Value]):
    """An environment maps from names (strings) to 
    some value type, which is specified in the constructor. 
    A default value can be provided for unmapped names. 
    """

    def __init__(self,  value_type: Type, default_value: Value):
        self._map = {}
        self.default_value = default_value
        self.value_type = value_type
        assert isinstance(default_value, self.value_type), "Default value should be of type {}".format(value_type)

    def __repr__(self) -> str:
        """repr(Env) doesn't look like constructor"""
        return "Env[{}]{}".format(self.value_type.__name__, self._map)

    def clear(self):
        """Clear all (name, value) pairs from the macp, 
        like the 'Clear Memory' key on a calculator.
        """
        self._map = {}

    def put(self, name: str, val: Value):
        """Add mapping (name, val), replacing any prior
        association with name.
        """
        log.debug("Storing {} to variable {}".format(val, name))
        assert isinstance(val, self.value_type), "Can't save value of type {}, only {}".format(
            type(val), self.value_type)
        self._map[name] = val

    def get(self, name: str) -> Value:
        """Returns current association of name.  If name is 
        not mapped, return default value. 
        """
        if name in self._map:
            return self._map[name]
        return self.default_value

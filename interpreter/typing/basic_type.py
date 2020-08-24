from interpreter.basic_object import BasicObject
from interpreter.basic_value import BasicValue
from interpreter.function import BuiltinFunction

class BasicType(BasicObject):
    REPR_FUNCTION_NAME = 'to_str'

    def __init__(self, parent=None, members={}, nominative=True):
        BasicObject.__init__(self, parent, members)
        self.nominative = nominative

    @property
    def type_name(self):
        return self.members['name']

    @property
    def friendly_typename(self):
        if 'name' in self.members:
            if isinstance(self.members['name'], BasicValue):
                return self.members['name'].extract_value()
            else:
                return self.members['name']

        return repr(self)

    def compare_type(self, other_type, parent_lookup=True):
        if other_type == self:
            return True

        if self.compare_value(other_type):
            return True

        if parent_lookup and self.parent is not None:
            circular = other_type.parent.parent == other_type

            return self.compare_type(other_type.parent, parent_lookup=(not circular))

        return False

    def has_property(self, name, property_type=None, limit=False):
        if name in self.members:
            return True

        if limit or self.parent is None:
            return None

        return self.parent.has_property(name, property_type)

    def get_property_type(self, name, limit=False):
        if name in self.members:
            return self.members[name]

        if limit or self.parent is None:
            return None

        return self.parent.get_property_type(name)

    def __repr__(self):
        return "BasicType({})".format(repr(self.members))

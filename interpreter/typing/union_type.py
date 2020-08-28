from interpreter.typing.basic_type import BasicType

class UnionType(BasicType):
    def __init__(self, lhs, rhs):
        BasicType.__init__(self, None, {}, False)
        self.lhs = lhs
        self.rhs = rhs

    def compare_value(self, other_type):
        return self.lhs.compare_value(other_type) or self.rhs.compare_value(other_type)

    def has_property(self, name, property_type=None):
        return self.lhs.has_property(name, property_type) or self.rhs.has_property(name, property_type)

    def get_property_type(self, name):
        if self.lhs.has_property(name):
            if (self.rhs.has_property(name)):
                return UnionType(self.lhs.get_property_type(name), self.rhs.get_property_type(name))
            else:
                return self.lhs.get_property_type(name)

        if self.rhs.has_property(name):
            return self.rhs.get_property_type(name)

        return None

    def __repr__(self):
        return "UnionType({}, {})".format(repr(self.lhs), repr(self.rhs))

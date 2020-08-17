from interpreter.basic_object import BasicObject
from interpreter.function import BuiltinFunction

def builtin_type_repr(arguments):
    interpreter = arguments[0]
    node = arguments[1]
    this_object = arguments[1]

    # TODO: return a string wrapped object?
    # TODO: each member should have a tagged type
    return "Type {\n" + '\n'.join(map(lambda x: "\t{},".format(x), this_object.members)) + "}" 

class BasicType(BasicObject):
    DEFAULT_TYPE_MEMBERS = {
        '__repr__': BuiltinFunction('__intern_type_repr__', None, builtin_type_repr)
    }

    def __init__(self, name, parent=None, members={}, nominative=False):
        BasicObject.__init__(self, parent, {**members, **BasicType.DEFAULT_TYPE_MEMBERS})
        self.name = name
        self.nominative = nominative

    def compare_type(self, other_type):
        if other_type == self:
            return True

        if self.nominative and self.name != other_type.name:
            return False

        if self.parent is None:
            if other_type.parent is not None:
                return False
        elif self.parent is not None:
            if other_type.parent is None:
                return False

        if not self.parent.compare_type(other_type.parent):
            return False

        for (mem_name, mem_type) in self.members.items():
            if not mem_name in other_type.members:
                return False
        
            if not mem_type.compare_type(other_type.members[mem_name]):
                return False

        return True

    def has_property(self, name, property_type=None):
        if not name in self.members:
            return False

        if property_type is not None:
            return property_type.compare_type(self.members[name])

        return True

    def get_property_type(self, name):
        if not name in self.members:
            return None

        return self.members[name]

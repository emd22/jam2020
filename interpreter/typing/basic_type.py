from interpreter.basic_object import BasicObject
from interpreter.basic_value import BasicValue
from interpreter.function import BuiltinFunction

class BasicType(BasicObject):
    REPR_FUNCTION_NAME = 'to_str'

    DEFAULT_TYPE_MEMBERS = {
        # REPR_FUNCTION_NAME: BuiltinFunction('__intern_type_repr__', None, builtin_type_repr)
    }

    def __init__(self, parent=None, members={}, nominative=True):
        BasicObject.__init__(self, parent, {**members, **BasicType.DEFAULT_TYPE_MEMBERS})
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

    # def compare_value(self, other_type, parent_lookup=True):

    #     #### TODO: 
    #     #### for comparing type to value, look up parent chain for value,
    #     #### comparing along the way

    #     if other_type == self:
    #         return True

    #     # if (self.nominative and self.type_name is not None) and self.type_name != other_type.type_name:
    #     #     print("name not eql: {} {}".format(self.type_name, other_type.type_name))
    #     #     return False

    #     # if self.parent is None:
    #     #     if other_type.parent is not None:
    #     #         return False
    #     # elif self.parent is not None:
    #     #     if other_type.parent is None:
    #     #         return False

    #     #     if not self.parent.compare_type(other_type.parent):
    #     #         return False

    #     for (mem_name, mem_type) in self.members.items():
    #         if mem_name == 'name': # skip because we use `nomanative` to decide this
    #             continue

    #         object_member = other_type.lookup_member(mem_name)
    #         print("value = {}".format(other_type))
    #         print("name = {}".format(mem_name))
    #         print("object_member = {}".format(object_member))

    #         if object_member is None:
    #             print("not in : {}".format(mem_name))
    #             return False
        
    #         print("mem_type {} = {}".format(mem_name, mem_type))
    #         if not mem_type.compare_value(object_member.value):
    #             print("not   : {}    {}".format(mem_type, object_member.value))
    #             return False

    #     # if other_type.parent is not None:
    #     #     #circular = other_type.parent.parent == other_type
    #     #     return self.compare_type(other_type.parent)

    #     return True

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
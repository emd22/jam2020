from interpreter.function import BuiltinFunction
from interpreter.basic_value import BasicValue
from parser.node import NodeFunctionExpression

class ObjectMember:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class BasicObject(BasicValue):
    def __init__(self, parent=None, members={}):
        BasicValue.__init__(self, None)
        self.parent = parent
        self.members = members

    def compare_value(self, other):
        if other == self:
            return True

        if not isinstance(other, BasicObject):
            return False

        for (mem_name, mem_value) in self.members.items():
            object_member = other.lookup_member(mem_name)

            if object_member is None:
                return False

            if not mem_value.compare_value(object_member.value):
                return False
        
        return True

    def extract_value(self):
        return self

    def extract_basicvalue(self):
        return self

    def lookup_type(self, global_scope):
        if self.parent is not None:
            return self.parent

        # BasicValue lookup_type call - resolves to Object usually
        return super.lookup_type(global_scope)

    def clone(self, parent_override=None):
        parent = self.parent

        if parent_override is not None:
            parent = parent_override

        members = {}

        for (key, value) in self.members.items():
            if isinstance(value, BasicValue):
                members[key] = value.clone()
            else:
                members[key] = value # this should actually just throw eventually unless it's a NodeFunctionExpression.

        return BasicObject(parent=parent, members=members)

    def assign_member(self, name, value):
        self.members[name] = value

    def lookup_member(self, name, member_type=None, parent_lookup=True):
        if name in self.members:
            if member_type is None or self.members[name].satisfies_type(member_type):
                return ObjectMember(name, self.members[name])
        #elif name == 'type':
        #    return ObjectMember('type', self.parent)
        elif parent_lookup and self.parent is not None:
            circular = self.parent.parent == self

            return self.parent.lookup_member(name, member_type, parent_lookup=parent_lookup and not circular)

        return None

    def satisfies_type(self, type):
        # all members are str -> BasicObject (or an extension thereof)
        for (tname, tvalue) in type.members.items():
            if self.lookup_member(tname, tvalue) is None:
                return False

        if type.parent is not None:
            return self.satisfies_type(type.parent)

        return True

    def union(self, other):
        from interpreter.typing.union_type import UnionType

        union_members = self.members.copy()

        for (name, value) in other.members.items():
            if name in union_members:
                if not value.compare_value(union_members[name]):
                    union_members[name] = UnionType(union_members[name], value)
        else:
            union_members[name] = value

        return BasicObject(None, union_members)

    def __repr__(self):
        return "BasicObject({})".format(repr(self.members))

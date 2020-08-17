from interpreter.function import BuiltinFunction

class ObjectMember:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class BasicObject:
    def __init__(self, parent=None, members={}):
        self.parent = parent
        self.members = members

    def clone(self, parent_override=None):
        parent = self.parent

        if parent_override is not None:
            parent = parent_override

        members = {}

        for (key, value) in self.members.items():
            members[key] = value.clone()

        return BasicObject(parent=parent, members=members)

    def assign_member(self, name, value):
        self.members[name] = value

    def lookup_member(self, name, member_type=None):
        if name in self.members:
            if member_type is None or self.members[name].satisfies_type(member_type):
                return ObjectMember(name, self.members[name])
        elif self.parent is not None:
            return self.parent.lookup_member(name, member_type)

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
                if not value.compare_type(union_members[name]):
                    union_members[name] = UnionType(union_members[name], value)
        else:
            union_members[name] = value

        return BasicObject(None, union_members)

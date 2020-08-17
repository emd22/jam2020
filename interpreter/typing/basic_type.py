from interpreter.basic_object import BasicObject

class BasicType(BasicObject):
    def __init__(self, name, parent=None, members={}, nominative=False):
        BasicObject.__init__(self, parent, members)
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

        for (mem_name, mem_type) in self.members:
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

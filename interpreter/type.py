

class Type:
  def __init__(self, name, parent=None, members={}, nominative=False):
    self.name = name
    self.parent = parent
    self.members = members
    self.nominative = nominative

    def union(self, other):
      return UnionType(self, other)

  # def merge(self, other, new_name):
  #   union_members = self.members.copy()

  #   for (name, value) in other.members:
  #     if name in union_members:
  #       if not value.compare_type(union_members[name]):
  #         union_members[name] = UnionType(union_members[name], value)
  #     else:
  #       union_members[name] = value

  #   return Type(new_name, )

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
    
class UnionType(Type):
  def __init__(self, name, lhs, rhs):
    self.name = name
    self.lhs = lhs
    self.rhs = rhs

  def compare_type(self, other_type):
    # TODO test this, might have to compare lhs,rhs as one against other_type.
    return self.lhs.compare_type(other_type) or self.rhs.compare_type(other_type)

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
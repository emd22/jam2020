### Custom types

Did you know...
You can create your own custom
types, just like `int`?

Types are objects just like
everything else in the language.
Objects can have properties of
many different forms.

To create your own type, use the
syntax:

```
let Person: type = {
  instance: {
    name: str;
  }
};
```

The reason we have the `instance`
property on the type is to show
the language which properties should
be `copied` onto new objects.
This functionality is called prototypical
inheritance.

You can have properties that persist
for all objects of a specific type,
as well. This is useful for declaring
methods that many similar objects can
use.

For example:

```
let Person: type = {
  instance: {
    name: str;
  },

  func say_hello(self) {
    print("hello from: ");
    print(self.name);
  }
};
```

In usage:
```
person_a = Person.new();
person_a.name = "Ron";

person_b = Person.new();
person_b.name = "Leslie";

person_a.say_hello(); # prints 'hello from: Ron'
person_b.say_hello(); # prints 'hello from: Leslie'
```

You can use the pseudo-property `type` on an object
to retrieve the object which it is based upon.

For example, the code `person_a.type` would
return `Person`, and the code `Person.type` would
give you the `Type` object, which all types are based upon.

Type 'inheritance' for information on type inheritance,
and extending custom or builtin types to add new properties,
or methods.

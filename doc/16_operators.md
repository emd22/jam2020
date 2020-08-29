### Available operators + Operator overloading

In the `iterators` section, we briefly spoke about how you can create
your own iteratable objects by means of adding a method named
`__iterate__` to your objects.

You'll be pleased to know that there are many more methods like this!
Every operator in the language (like '+', '-', '*', '!=', etc...) is
evaluated at runtime by calling a corresponding method.

Some examples of what method names operators are paired with are:
* `+` - `__add__`
* `-` - `__sub__`
* `*` - `__mul__`
* `/` - `__div__`
* `%` - `__mod__`
* `==` - `__eql__`
* `!=` - `__noteql__`
* `!` - `__not__`
* `<=>` - `__compare__` (spaceship operator: return -1 if less than, 0 if equal, 1 if greater than)
* `<` - `__lt__` (defaults to `(self <=> other) == -1;`)
* `<=` - `__lte__` (defaults to `(self <=> other) != 1;`)
* `>` - `__gt__` (defaults to `(self <=> other) == 1;`)
* `>=` - `__gte__` (defaults to `(self <=> other) != -1;`)
* `&` - `__bitand__`
* `|` - `__bitor__`
* `^` - `__bitxor__`
* `&&` - `__and__`
* `||` - `__or__`
* `()` (function call) - `__call__`
* `if ...` (boolean conversion) - `__bool__`
* `for x in ...` (iteration) - `__iterate__`

If you add these methods to your objects, you can actually use common
operators on them just like you would with numbers or other built-in
standard objects.

Here's an example of how you can use (and abuse) operator overloading

```
let Person = Type.extend({
    instance = {
        name
    }

    func __construct__(self, name) {
        self.name = name;
    }

    func __add__(self, other) {
        return Person.new(self.name + ' ' + other.name);
    }
})

let person1 = Person.new('Johnny');
let person2 = Person.new('Storm');

print(person1 + person2); # prints 'Johnny Storm'
```

If you look at some of the built in types such as `std/types/int`,
you'll see how these methods work in action!

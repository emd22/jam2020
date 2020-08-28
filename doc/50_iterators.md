### Building custom iterator objects

If you looked at the `arrays` walkthrough,
you learned how you can use `for` loops to walk
over the contents of an array.

While the `for` loop is powerful, in some instances
other types of loops may be called for. 

The `while` loop allows us to execute a block _until_
a condition we give it has been reached. Here's an example.

```
let value = 10;
while value != 5 {
    print(value);
    value -= 1;
}
```

Prints:
```
10
9
8
7
6
```

Easy peasy!

Did you know you can create your own iteratable objects, much
like how array works in the `for` loop?

Simply add a method to your object called `__iterate__`, taking
a single argument (along with the `self` argument). This argument
represents a callback that you will feed the current value of your
iterator into. Take a look in `std/types/array` to see for yourself!
      """),

      'operators': ('Builtin operators, operator overloading', """
In the `loops` section, we briefly spoke about how you can create
your own iteratable objects by means of adding a method named
`__iterate__` to your objects.

You'll be pleased to know that there are many more methods like this!
Every operator in the language (like '+', '-', '*', '!=', etc...) is
evaluated at runtime by calling a corresponding method.

Some examples of what method names operators are paired with are:
'+' - '__add__'
'-' - '__sub__'
'*' - '__mul__'
'/' - '__div__'

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

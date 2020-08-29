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

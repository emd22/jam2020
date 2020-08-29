### Strings operations and interpolation

PEACH includes some built-in operations you
can use to manipulate and format strings.
If you look at `std/types/str.peach`, you'll
notice several useful methods such as:

* `append`: Join two strings together
* `__mul__` (operator overload for the `*` operator): Repeat strings
    Example: `"Hello " * 3` returns `"Hello Hello Hello "
* `to_int`: Parse a string into an integer
* `format`: String interpolation, using `%` as the substitute character.
    Example:
      `"My name is % and I am % years old".format('Bob', '15');`
      
You'll also notice that the `Str` type is extended from
`Array`. This is because a string is essentially an array, but for
characters. Basing the `Str` type from `Array` allows us to use any `Array` methods such as `len`, `__at__` (the `[]` operator), `find`, `map`, `contains` and more.

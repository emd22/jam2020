### Random number generation

PEACH includes a module for generating random numbers, `std/math/random`.
You can use this module to generate a random integer from a seed value,
or you can use the `range` function of `Random` to generate a random
number from a predefined range of your choice.

Example:

```
import "std/math/random.peach";
print(Random.range(1337, 25, 1)); #* prints 10  -- try with a different seed! *#
```

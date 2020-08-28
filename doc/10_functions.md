### Writing and calling functions

In programming, a function is a reusable piece of code
done to perform a certain task. Functions can optionally
take in parameters (called arguments) and usually return an output.

For a function with no arguments, assuming the name of the
function is `calculate`, you would call it like this:
`calculate();`

To pass arguments, say, two numbers to add together, you would
instead call it like this:
`calculate(5, 10);`

We can declare our own functions, as well! This piece of
code would create our calculate function, which would simply
add the two given numbers together.

```
func calculate(first: int, second: int) {
  return first + second;
};
```

Try creating the calculate function and calling it
  -- watch the output change depending on what numbers you
      pass in as `first` and `second`!

Functions can also be used as expressions. This allows
us to reassign functions and swap out object methods at
runtime. For example, to swap out the calculate method:

```
calculate = func (first: int, second: int) {
  return first * second;
}
```

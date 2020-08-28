### Console input and output

To read and write to and from the console,
the `io` module includes a few built-in methods 
extended from the `Console` object.

The `io` module is included by default as
it is imported from within the
standard __core__ module, so you don't have to
import any modules manually in order to start using
it.

To print to the console:
`io.write('your string here');`

And to read input from the console:

```
let response = io.read(); # read user input and store in `response`
io.write(response);       # print it back out to the console
```

You can also print to the console in a few different colors!
Here's an example on how to do that:

```
io.write_color(Console.BLUE, "I'm blue ba ba dee ba ba die");
```

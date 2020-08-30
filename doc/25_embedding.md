### Embedding

During the development of a program you may want
to use PEACH code in Python to interface between the
two languages. For this, we added a few important modules
in the `Peach` class to help interface with PEACH.

The `Peach.call_function` method takes in the name of the function
and a list containing arguments to be passed into the language.
`call_function` returns the Python value of the internal return
value in PEACH. For example, calling `math.sqrtf` with arguments
`[25]` would result in a value of `5.0` in Python.

The `Peach.eval`, `Peach.eval_data`, and `Peach.eval_file` methods
all take data passed in and evaluate them as PEACH code. For example,
if we write `peach.eval_data('print("Hello, %!".format("World"));')`,
`eval_data` would call PEACH function `print`, call `str.format` on
`'Hello, %!'`, and output value to terminal.
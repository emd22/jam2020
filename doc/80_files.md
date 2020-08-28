### File reading and writing

At some point in your program or script you will
likely want to make use of file input and output.
Wheather you're reading and saving configuration
files, or a user's documents, file I/O can be
very useful.

Just like the `Console` object, a `File` object is
also made available by means of the `io` module.
The `io` module is imported from the standard
`__core__` module and thus available without any
manual importing.

To write a string to a file, use the `File.write` method.
This method takes in two arguments: The path to the file
you want to write, as well as the content you want to write
to the file.

Example:
```
File.write('file.txt', 'Hello world');
```

To open a file, we create `File` instance object via
the `File.open` method. An instance of the `File`
object holds the name and path of the file, as
well as the actual data it holds.

Here is an example of how to read a file into a variable.

```
let file = File.open('file.txt');
let content = file.data;

Console.write(content); # write output to console
```

### Modules

Sometimes, especially in large projects,
you will want to pull in code from other files.
Maybe it's a function that is part of a library
you downloaded or it could be your own code.

Separating code into different files allows us
to create cleaner code by segmenting ideas
and functionality into separate consumable
units.

Let's get started by showing how to 'import'
a module from a separate file.

We use the 'import' keyword along with a string
of text which points to the path of the file
we wish to use.

Say you want to write some text to the console.
You can use our standard `io` package, provided
with the language, by writing this line of code:

`import "std/io.kb";`

Easy, right? Now you can use the `print` function!

Try it for yourself:
`print("hello world");`

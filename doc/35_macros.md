### Macros

Macros allow you to write code that generates more code. When you evaluate a macro,
it's code is inserted directly into the spot which it is used. Macros allow you to 
manipulate the code that they generate from within PEACH.

Use the `macro` keyword to declare a macro, along with any arguments the
macro may take, much like declaring a function. From within the body of
the macro, you can use the `mixin` keyword along with a block of code
to tell the language to insert the code here.

Example:
```
macro print_times(text: str, times: int) {
  for i in Range.new(0, times) {
    mixin {
      print(str);
    }
  }
}
```

Usage:
```
print_times("hello world!", 5)();

# alternatively, this works
# print_times("hello world!", 5).expand();

# hello world!
# hello world!
# hello world!
# hello world!
# hello world!
```

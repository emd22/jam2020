### Building custom iterator objects

If you looked at the `arrays` walkthrough,
you learned how you can use `for` loops to walk
over the contents of an array.

While the `for` loop is powerful, in some instances you may want to allow your own custom types and objects to be used in a `for` loop.

If you look at the `__iterate__` method in `std/types/array.peach` you'll see how the `Array` type handles for loops.

```
# std/types/array.peach

func __iterate__(self, cb: Func) {
  let remaining = self.len();
  let len = self.len();

  while remaining != 0 {
    let index = len - remaining;

    cb(self[index]);

    remaining -= 1;
  }
}
```

The `cb` parameter is a callback function which `for` internally uses to hand off execution to the block that was provided for the `for` loop.

You can think of this as a generator of sorts if you're familiar with that from other languages.



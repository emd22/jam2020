### Extending types using prototypical inheritance

When you want to add functionality to an existing type, but
only in specialized use cases, you'll want to know how to
extend a type!

Extending a type means you can keep the existing functionality a
type has to offer, while still being able to add new functionality
without cluttering up the original type.

An example being, we take our `Person` type from the previous `types`
example section, and add two new subclasses - one being for a `Customer`,
a little more specific than just being an average person, and
one being `Employee`, yet again a bit more defined than just being a person.

Since `Person` already has the `name` property, and both customers and
employees can have names, we'll make use of this existing
functionality and not have to write the same code again twice.

Here is an example on how to create our `Customer` and `Employee` types.

```
let Customer: type = Person.extend({
  instance = {
    customer_id: str;
  }
});

let Employee: type = Person.extend({
  instance = {
    employee_id: str;
    job_title: str;
  }
});
```

We can still even use the say_hello method from `Person`!
That's the power that inheritance has to offer.

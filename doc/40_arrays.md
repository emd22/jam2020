### Array operations

In your code, you may want to store multiple
contiguous objects together, such as a list
of names, products, etc. Arrays let you do this
in a way that won't clutter up your code with
lots of related variable names.

Arrays are also dynamically expandable, meaning
you can add and remove data from them as you please.
They can be manipulated in several ways, such as 
mapping each item in an array to a new item by means
of transforming it via a function.

Arrays can be iterated over one-by-one by using the
`for` loop -- more info on that in the `interators` section.

Here's an example of how to create an array and assign
it to a variable.

`let names = ['Jeffrey', 'Sam', 'Buddy'];`

The `names` array holds three strings, each
representing a name.

If you want to loop over these names, you can use `for`.

```
for name in names {
    print(name);
}
```

Prints:
```
Jeffrey
Sam
Buddy
```


To access a specific item in an array by index, use the
access operator (square brackets)

`print(names[1]); # prints 'Sam'`

Arrays have multiple methods, including ways of checking whether
an object is contained by the array, appending new items to
an array, and creating unions or intersections with other arrays.

```
names.contains('Buddy'); # true
names.append('Tiffany'); # names is now ['Jeffrey', 'Sam', 'Buddy', 'Tiffany']

names.union(['Sam', 'Tyler']) # returns ['Jeffrey', 'Sam', 'Buddy', 'Tyler']
names | ['Sam', 'Tyler'] # returns ['Jeffrey', 'Sam', 'Buddy', 'Tyler']

names.intersection(['Sam', 'Tyler']) # returns ['Sam']
names & ['Sam', 'Tyler'] # returns ['Sam']
```

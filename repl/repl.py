from lexer import Lexer, TokenType, LexerToken
from parser.parser import Parser
from parser.node import AstNode, NodeType
from parser.source_location import SourceLocation
from interpreter.interpreter import Interpreter
from interpreter.env.builtins import obj_to_string
from error import InterpreterError
from ast_printer import AstPrinter
from util import LogColour

# when including readline, it switches input() over and allows
# text seeking and other cool things
import readline

import signal

class Repl:
    REPL_FILENAME = '<repl>'
    
    WALKTHROUGH_MESSAGES = {
        'vars': ('How to declare and use variables', """
  To get started with variables,
  use the `let` keyword. To use
  `let`, we give the name we
  want to be associated with
  the variable, as well as an
  optional type, such as `int`,
  `float`, or `str`.

  For example:

  `let mynum: int = 5;`

  Creates a variable named mynum,
  with a type of `int`, and assigns
  its value to 5.
        """),

        'functions': ('Writing and calling functions', """
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
  let calculate: func = (first, second) {
    return first + second;
  };
  ```

  Try creating the calculate function and calling it
    -- watch the output change depending on what numbers you
       pass in as `first` and `second`!

        """),

        'types': ('Custom types, prototypical inheritance', """
  Did you know...
  You can create your own custom
  types, just like `int`?

  Types are objects just like
  everything else in the language.
  Objects can have properties of
  many different forms.

  To create your own type, use the
  syntax:

  ```
  let Person: type = {
    instance: {
      name: str;
    }
  };
  ```

  The reason we have the `instance`
  property on the type is to show
  the language which properties should
  be `copied` onto new objects.
  This functionality is called prototypical
  inheritance.

  You can have properties that persist
  for all objects of a specific type,
  as well. This is useful for declaring
  methods that many similar objects can
  use.

  For example:

  ```
  let Person: type = {
    instance: {
      name: str;
    },
    say_hello: func = (self) {
      print("hello from: ");
      print(self.name);
    }
  };
  ```

  In usage:
  ```
  person_a = Person.new();
  person_a.name = "Ron";

  person_b = Person.new();
  person_b.name = "Leslie";

  person_a.say_hello(); # prints 'hello from: Ron'
  person_b.say_hello(); # prints 'hello from: Leslie'
  ```

  You can use the pseudo-property `type` on an object
  to retrieve the object which it is based upon.

  For example, the code `person_a.type` would
  return `Person`, and the code `Person.type` would
  give you the `Type` object, which all types are based upon.

  Type 'inheritance' for information on type inheritance,
  and extending custom or builtin types to add new properties,
  or methods.
        """),

        'inheritance': ('Extending types using Type.extend', """
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
        """),



        'arrays': ('Using arrays', """
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
  `for` loop -- more info on that in the `loops` section.

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


  To access a specific item in an array by index, use the
  access operator (square brackets)

  `print(names[1]); # prints 'Sam'`
  ```

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
        """),

        'loops': ('Loops and iterators', """
  If you looked at the `arrays` walkthrough,
  you learned how you can use `for` loops to walk
  over the contents of an array.

  While the `for` loop is powerful, in some instances
  other types of loops may be called for. 

  The `while` loop allows us to execute a block _until_
  a condition we give it has been reached. Here's an example.

  ```
  let value = 10;
  while value != 5 {
      print(value);
      value -= 1;
  }
  ```

  Prints:
  ```
  10
  9
  8
  7
  6
  ```

  Easy peasy!

  Did you know you can create your own iteratable objects, much
  like how array works in the `for` loop?

  Simply add a method to your object called `__iterate__`, taking
  a single argument (along with the `self` argument). This argument
  represents a callback that you will feed the current value of your
  iterator into. Take a look in `std/types/array` to see for yourself!
        """),

        'operators': ('Builtin operators, operator overloading', """
  In the `loops` section, we briefly spoke about how you can create
  your own iteratable objects by means of adding a method named
  `__iterate__` to your objects.

  You'll be pleased to know that there are many more methods like this!
  Every operator in the language (like '+', '-', '*', '!=', etc...) is
  evaluated at runtime by calling a corresponding method.

  Some examples of what method names operators are paired with are:
  '+' - '__add__'
  '-' - '__sub__'
  '*' - '__mul__'
  '/' - '__div__'

  If you add these methods to your objects, you can actually use common
  operators on them just like you would with numbers or other built-in
  standard objects.

  Here's an example of how you can use (and abuse) operator overloading

  ```
  let Person = Type.extend({
      instance = {
          name
      }

      func __construct__(self, name) {
          self.name = name;
      }

      func __add__(self, other) {
          return Person.new(self.name + ' ' + other.name);
      }
  })

  let person1 = Person.new('Johnny');
  let person2 = Person.new('Storm');

  print(person1 + person2); # prints 'Johnny Storm'
  ```

  If you look at some of the built in types such as `std/types/int`,
  you'll see how these methods work in action!
        """),


        'ranges': ('Ranges', ''),

        'modules': ('Using code from other files + using the `io` module', """
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
        """),


        'console': ('Console input and output', """
  To read and write to and from the console,
  we've added an object called `Console`
  to the `io` module.

  The `io` module is included by default as
  it is imported from within the
  standard __core__ module, so you don't have to
  import any modules manually in order to start using
  it.

  To print to the console:
  `Console.write('your string here');`

  And to read input from the console:

  ```
  let response = Console.read(); # read user input and store in `response`
  Console.write(response);       # print it back out to the console
  ```
        """),

        'files': ('File reading and writing', """
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
        """)
    }

    def __init__(self):
        self.interpreter = Interpreter(SourceLocation(Repl.REPL_FILENAME))
        self.repl_import_defaults()
        signal.signal(signal.SIGINT, self.at_exit)
        
    def at_exit(self, signal, frame):
        print('\nExiting...')
        exit(0)
        
    def repl_import_defaults(self):
        # tmp_lexer = Lexer(0, SourceLocation(Repl.REPL_FILENAME))
        # tmp_parser = Parser(tmp_lexer)
        # generate import nodes
        repl_import_nodes = [
            Parser.import_file(Parser, 'std/__core__.peach'),
            Parser.import_file(Parser, 'std/__repl__.peach')
        ]

        # if len(tmp_parser.error_list.errors) > 0:
        #     tmp_parser.error_list.print_errors()
        # else:
        # eval asts
        self.eval_line_ast(repl_import_nodes)
        
    def loop(self):
        print(REPL_WELCOME_MESSAGE)
        
        while True:
            self.accept_input()

    def accept_input(self):
        line = ""
        
        line = input('>>> ')

        trimmed = line.strip()
        if trimmed in Repl.WALKTHROUGH_MESSAGES:
            print(Repl.WALKTHROUGH_MESSAGES[trimmed][1])

            return

        (brace_counter, bracket_counter, paren_counter) = self.count_continuation_tokens(line)

        while brace_counter > 0 or bracket_counter > 0 or paren_counter > 0:
            next_line = input('... ')
            line += next_line + '\n'
            (brace_counter, bracket_counter, paren_counter) = self.count_continuation_tokens(line)

        (line_ast, error_list) = self.parse_line(line)

        # for node in line_ast:
        #     AstPrinter().print_ast(node)

        if len(error_list.errors) > 0:
            error_list.print_errors()
            return
            
        self.eval_line_ast(line_ast)

    def eval_line_ast(self, line_ast):
        last_value = None
        last_node = None

        for node in line_ast:
            last_node = node
            try:
                last_value = self.interpreter.visit(node)
            except InterpreterError:
                self.interpreter.error_list.clear_errors()
                continue

        if last_value is not None:
            obj_str = obj_to_string(self.interpreter, last_node, last_value)
            print(f"{LogColour.Info}{obj_str}{LogColour.Default}")

    def parse_line(self, line):
        lexer = Lexer(line, SourceLocation(Repl.REPL_FILENAME))
        lexer.lex()

        parser = Parser(lexer)
        
        return (parser.parse(), parser.error_list)

    def count_continuation_tokens(self, line):
        brace_counter = 0
        bracket_counter = 0
        paren_counter = 0

        for ch in line:
            if ch == '{':
                brace_counter += 1
            elif ch == '}':
                brace_counter -= 1
            elif ch == '(':
                paren_counter += 1
            elif ch == ')':
                paren_counter -= 1
            elif ch == '[':
                bracket_counter += 1
            elif ch == ']':
                bracket_counter -= 1

        return (brace_counter, bracket_counter, paren_counter)

REPL_WELCOME_MESSAGE = """
----- R E P L C E P T I O N -----

  An interactive console that
  allows you to write quick
  statements and learn more about
  how the language works.

            ------

  Let's get started!
  To learn more about the language,
  type one of the following:

  {}

---------------------------------
    """.format('\n  '.join(map(lambda key: "{}--  {}".format(key.ljust(16), Repl.WALKTHROUGH_MESSAGES[key][0]), Repl.WALKTHROUGH_MESSAGES)))

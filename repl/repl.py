from lexer import Lexer, TokenType, LexerToken
from parser.parser import Parser
from parser.node import AstNode, NodeType
from parser.source_location import SourceLocation
from interpreter.interpreter import Interpreter
from error import InterpreterError
from ast_printer import AstPrinter
from util import LogColour

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
        """),

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
        """)
    }

    def __init__(self):
        self.interpreter = Interpreter(SourceLocation(Repl.REPL_FILENAME))

    def loop(self):
        print(REPL_WELCOME_MESSAGE)

        while True:
            self.accept_input()

    def accept_input(self):
        line = input('>>> ')

        trimmed = line.strip()
        if trimmed in Repl.WALKTHROUGH_MESSAGES:
            print(Repl.WALKTHROUGH_MESSAGES[trimmed][1])

            return

        (brace_counter, bracket_counter, paren_counter) = self.count_continuation_tokens(line)

        while brace_counter > 0 or bracket_counter > 0 or paren_counter > 0:
            next_line = input()
            line += next_line + '\n'
            (brace_counter, bracket_counter, paren_counter) = self.count_continuation_tokens(line)

        (line_ast, error_list) = self.parse_line(line)

        # for node in line_ast:
        #     AstPrinter().print_ast(node)

        if len(error_list.errors) > 0:
            error_list.print_errors()
            return

        last_value = None

        for node in line_ast:
            try:
                last_value = self.interpreter.visit(node)
            except InterpreterError:
                continue

        if last_value is not None:
            print(f"{LogColour.Info}{repr(last_value)}{LogColour.Default}")

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
    """.format('\n  '.join(map(lambda key: "{}\t\t--  {}".format(key, Repl.WALKTHROUGH_MESSAGES[key][0]), Repl.WALKTHROUGH_MESSAGES)))
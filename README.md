## PEACH - Prototypical language with knack for extensibility and meta programming

In PEACH, all types are objects, and vice versa. Everything is an object, and that includes functions. Objects descend from a parent object and inherit functions and variables from the parent. For example, to create a type, we extend from a parent `Object` (in this case `Type`), and define any methods

The core library in PEACH is written in itself, even allowing for methods to be attached with the `Object.patch()` method at runtime. Types in PEACH are built of `Object`s and have overloadable functions for operations such as addition, subtraction, multiplication, division, modulus, and compare. Types including String, Int, Float, and Bool are all defined completely in PEACH, including all operations that can be done on them. For instance, the call operator can be overloaded, with an example being that when a Number is called `5(10)` it multiplies the values together, allowing for a math-like syntax in programming.

PEACH also has many methods that have functional language characteristics for example Array mapping and lambdas, and new concept ideas such as [Prototypical Inheritance](https://en.wikipedia.org/wiki/Prototype-based_programming). 

Later we plan to rewrite PEACH in C/C++ for better speed, efficiency. Both of us have more experience in C/C++. We plan to keep PEACH code and the standard library similar to how it is today.

[vars](./doc/00_vars.md) - How to declare and use variables

[functions](./doc/10_functions.md) - Writing and calling functions

[strings](./doc/15_strings.md) - Strings operations and interpolation

[operators](./doc/16_operators.md) - Available operators + Operator overloading

[types](./doc/20_types.md) - Custom types

[proto](./doc/30_proto.md) - Extending types using prototypical inheritance

[macros](./doc/35_macros.md) - Macros

[arrays](./doc/40_arrays.md) - Array operations

[iterators](./doc/50_iterators.md) - Building custom iterator objects

[random](./doc/55_random.md) - Random number generation

[modules](./doc/60_modules.md) - Modules

[console](./doc/70_console.md) - Console input and output

[files](./doc/80_files.md) - File reading and writing


### Examples

...

Be sure to check out our TicTacToe example!
Start the REPL by running `main.py` and call `tictactoe();` to try it out!

```
let ttt = Type.extend({
    name = "TicTacToe"
    
    EMPTY = 0
    O_SPOT = 1
    X_SPOT = 2
    
    instance = {
        moves = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        func to_str(self) {
            return "TicToeToe moves: " + self.moves.to_str();
        }
    }
    func __construct__(self){
    }
    
    play = func (self){}
    board_gen = func (self){}
    
    func board_draw_top(self){
    }
    
    func get(self, loc) {
        let strn = loc+1;
        let ch:str = strn.to_str();
        let move = self.moves[loc].to_int();
        if  move == self.O_SPOT {
            ch = 'O';
        }
        elif move == self.X_SPOT {
            ch = 'X';
        }
        return ch;
    }
    
    func clear_board(self) {
        self.moves = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    }
    
    func ai_find_next_spot(self) {
        import "std/time.peach";
        import "std/math/random.peach";
        
        let available_spaces = [];
        let index = 0;
        for move in self.moves {
            if move == 0 {
                available_spaces += index;
            }
            index += 1;
        }
        if available_spaces == [] {
            print("Tied!");
            self.clear_board();
            self.ai_find_next_spot();
            return 0;
        }
        
        let rand = random.range(Time.now().to_int(), available_spaces.len()-1, 0);
        self.moves[available_spaces[rand]] = self.O_SPOT;
    }
    
    func ai_move(self) {
        return self.ai_find_next_spot();
    }
    
    func check_index(self, player, center_index, offset, check_offset) {
        let index = 0;
        
        while index != 3 {
            if self.moves[center_index-check_offset] == player {
                if self.moves[center_index+check_offset] == player {
                    if self.moves[center_index] == player {
                        return player;                    
                    }
                }
            }
            center_index += offset;

            index += 1;
        }
        return self.EMPTY;
    }
    
    func check_diag_corner(self, player, top, bottom) {
        if self.moves[top] == player {
            if self.moves[bottom] == player {
                if self.moves[4] == player {
                    return player;
                }
            }
        }
        return self.EMPTY;
    }
    
    func check_diagonal(self, player) {

        let tl = self.check_diag_corner(player, 0, 8);
        let bl = self.check_diag_corner(player, 6, 2);
        if tl {
            return tl;
        }
        if bl {
            return bl;
        }
        return self.EMPTY;
    }
    
    func print_winner(self, player) {
        if player == self.O_SPOT {
            print("");
            print("=== YOU LOSE! ==="); 
            print("");
        }
        elif player == self.X_SPOT {
            print("");
            print("=== YOU WIN! ===");
            print("");
        }
    }
    
    func check_winner(self, player) {
        # start at left side in middle of board, checking above and below, and move by 1 spot.
        let colcheck = self.check_index(player, 3, 1, 3);
        # start at top in middle of board, checking left and right and moving down by board width
        let rowcheck = self.check_index(player, 1, 2, 1);

        let diagcheck = self.check_diagonal(player);
        
        # check if win in columns
        if colcheck {
            self.print_winner(player);
            self.clear_board();
            return true;
        }
        # check if win in rows
        elif rowcheck {
            self.print_winner(player);
            self.clear_board();
            return true;
        }
        # check if win in diagonal spaces
        elif diagcheck {
            self.print_winner(player);
            self.clear_board();
            return true;
        }

        return false;
    }
    func player_write(self, player_char) {
        if player_char == 'O' {
            io.write_color(Console.RED, player_char);
        }
        elif player_char == 'X' {
            io.write_color(Console.YELLOW, player_char);
        }
        else {
            io.write(player_char);
        }
    }

    func board_draw_row(self, lc) {
        let v0 = self.get(lc);
        let v1 = self.get(lc + 1);
        let v2 = self.get(lc + 2);

        # print column 1
        io.write("| "); self.player_write(v0);
        # column 2
        io.write(" | "); self.player_write(v1);
        # column 3
        io.write(" | "); self.player_write(v2);
        # print end
        io.write(" |\n");

        print("+---+---+---+");
    }
    
    func board_draw(self) {
        let index = 0;
        print("+---+---+---+");
        while index != 9 {
            self.board_draw_row(index);
            index += 3;
        }
    }
});

ttt.play = func (self) {
    let command = "";
    
    print("=== TICTACTOE ===");
    print("Input 'q' to exit");
    print("Input a number play a spot");
    self.board_draw();
    
    let int_cmd = 0;
    
    while command != "q" {
        command = Console.read();
        if command == 'q' {
            return 0;
        }
        int_cmd = command.to_int()-1;
        if self.moves[int_cmd] == self.EMPTY {
            self.moves[int_cmd] = self.X_SPOT;            
            self.check_winner(self.X_SPOT);
            self.ai_move();
            self.check_winner(self.O_SPOT);
            self.board_draw();
        }
        else {
            print("Space already taken!");
            self.board_draw();
        }
    }
};

```

#!/bin/python3

from peach import Peach
from parser.parser import Parser
from examples.embed import example_embed

import sys

def main():
    peach = Peach()

    if len(sys.argv) <= 1:
        peach.repl()
        return

    filename = sys.argv[1]
    peach.eval_file(filename)
    value = peach.call_function('math.sqrt', [25])
    arg_cnt = peach.call_function('print', [value])
    example_embed(peach)

if __name__ == '__main__':
    main()

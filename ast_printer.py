from parser.node import AstNode, NodeType

class AstPrinter:
    def print_func(self, string, indent_level):
        print((indent_level * '  ') + str(string))

    def print_tokens(self, lexer, indent_level):
        for token in lexer.tokens:
            self.print_func(token, indent_level)

    def print_ast(self, node, indent_level=0):
        if node == None:
            return
        
        self.print_func(node, indent_level)
        
        if node.type == NodeType.Block:
            for child in node.children:
                self.print_ast(child, indent_level + 1)
                
        elif node.type == NodeType.BinOp:
            # branch left & right
            self.print_ast(node.left, indent_level)
            self.print_ast(node.right, indent_level)
        
        elif node.type == NodeType.Assign:
            self.print_ast(node.lhs, indent_level)
            self.print_ast(node.value, indent_level)
            
        elif node.type == NodeType.Declare:
            self.print_ast(node.value, indent_level)
        elif node.type == NodeType.ArgumentList:
            self.print_func('(', indent_level)

            for argument in node.arguments:
                self.print_ast(argument, indent_level + 1)
                self.print_func(', ', indent_level + 1)

            self.print_func(')', indent_level)
        elif node.type == NodeType.FunctionExpression:
            self.print_func('<Function>', indent_level)
            self.print_ast(node.argument_list, indent_level)
            self.print_ast(node.block, indent_level)

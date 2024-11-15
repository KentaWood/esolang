import lark
import esolang.level1_statements


grammar = esolang.level1_statements.grammar + r"""
    %extend start: forloop
                 | whileloop

    forloop: "for" NAME "in" range block

    whileloop: "while" condition_loop block

    range: "range" "(" expr ")"

    condition_loop: expr comparison_op expr

    comparison_op: "<"  -> lt
                 | ">"  -> gt
                 | "<=" -> le
                 | ">=" -> ge
                 | "==" -> eq
                 | "!=" -> ne
"""
parser = lark.Lark(grammar)


class Interpreter(esolang.level1_statements.Interpreter):
    '''
    >>> interpreter = Interpreter()
    >>> interpreter.visit(parser.parse("for i in range(10) {i}"))
    9
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; a"))
    45
    >>> interpreter.visit(parser.parse("a=0; for i in range(10) {a = a + i}; i")) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
        ...
    ValueError: Variable i undefined
    '''
    def range(self, tree):
        # Evaluate the range expression and return a Python range object
        expr_value = self.visit(tree.children[0])
        if not isinstance(expr_value, int) or expr_value < 0:
            raise ValueError("Range must be a non-negative integer.")
        return range(expr_value)

    def forloop(self, tree):
        # Extract loop variable name, range expression, and block
        loop_var = tree.children[0].value
        loop_range = self.visit(tree.children[1])  # Evaluate range
        block = tree.children[2]

        # Add a new scope for the loop
        self.stack.append({})
        result = None

        # Iterate over the range, assigning values to the loop variable
        for value in loop_range:
            self.stack[-1][loop_var] = value  # Assign loop variable
            result = self.visit(block)  # Execute block

        # Remove loop scope
        self.stack.pop()
        return result
    

    def condition_loop(self, tree):
        left = self.visit(tree.children[0])
        right = self.visit(tree.children[2])
        op = tree.children[1].data

        if op == "lt":
            return 0 if left < right else 1
        elif op == "gt":
            return 0 if left > right else 1
        elif op == "le":
            return 0 if left <= right else 1
        elif op == "ge":
            return 0 if left >= right else 1
        elif op == "eq":
            return 0 if left == right else 1
        elif op == "ne":
            return 0 if left != right else 1
        else:
            raise ValueError(f"Unknown comparison operator: {op}")

    def whileloop(self, tree):
        condition = tree.children[0]
        block = tree.children[1]

        results = []  # Collect results from each iteration

        while self.visit(condition) == 0:  # Continue while condition is true (0)
            self.stack.append({})
            result = self.visit(block)  # Execute the block and capture the result
            self.stack.pop()

            # Add the result of this iteration to the results list
            results.append(result)

        return results  # Return all results from the loop iterations


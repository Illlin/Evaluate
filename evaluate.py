from typing import Optional, List


methods = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "/": lambda a, b: a / b,
    "*": lambda a, b: a * b,
}


def tokenise(expression: str, special_tokens="()+-*/") -> List[str]:
    """Returns a list of tokens"""
    # In the current grammar every special token is exactly 1 character long, and numbers can be any length
    # Read through string from left to right, building up tokens
    expression = expression.replace(" ", "")  # We can ignore all white space

    tokens = []
    running_string = ""  # Will store tokens longer than 1 char
    for char in expression:
        if char in special_tokens:
            # Need to add and clear running string
            if len(running_string) > 0:
                tokens.append(running_string)
                running_string = ""
            tokens.append(char)
        else:
            # This case is any number
            running_string += char

    # Check for trailing numbers
    if len(running_string) > 0:
        tokens.append(running_string)

    return tokens


def parse(tokens: List[str], operations="+-*/"):
    # Walk through the list of tokens into expressions, such as:
    # ["+", "3" ["+" ["1", "2"]]] for 1 + 2 + 3
    # Step 1, handle brackets
    # Error checking, count brackets
    if tokens.count("(") != tokens.count(")"):
        return None

    stack = []

    current_operation = ""
    while len(tokens) > 0:
        token = tokens.pop(0)
        if token == ")":
            return None  # Can't encounter a close before an open

        if token == "(":
            sub_tokens = []
            bracket_depth = 1
            while bracket_depth > 0:
                sub_token = tokens.pop(0)
                if sub_token == "(":
                    bracket_depth += 1
                if sub_token == ")":
                    bracket_depth -= 1
                sub_tokens.append(sub_token)
            # This will have an extra ")" hanging at the end
            sub_tokens.pop()
            sub_parse_tree = parse(sub_tokens)  # Recursivly parse
            if sub_parse_tree is None:
                return None
            # This is now one token
            stack.append(sub_parse_tree)
        elif token in operations:
            # Causes this to be handled after the next token
            current_operation = token
            continue
        else:
            stack.append(token)

        if current_operation != "":
            if len(stack) < 2:
                return None  # Error state, invalid function
            a = stack.pop()
            b = stack.pop()
            stack.append([current_operation, b, a])
            current_operation = ""
    if len(stack) > 1:
        return None  # Dangling operation, invalid expression, such as "(1 + 2) 3"
    return stack[0]  # The stack should have 1 item in it


def evaluate_parse_tree(parse_tree) -> Optional[int]:
    # Recursive function to parse
    # Two cases can occur. Either it is a list of 3 items, or 1 string
    if type(parse_tree) is str:
        return int(parse_tree)

    # In this case it is a list of three items where the first is the operation
    return methods[parse_tree[0]](
        evaluate_parse_tree(parse_tree[1]),
        evaluate_parse_tree(parse_tree[2])
    )


def evaluate(expression: str) -> Optional[int]:
    """Returns the result, or None if there was an error."""
    # The parsing and evaluation of the expression grammar will be split into 3 parts,
    # tokenisation, parsing, and evaluation
    tokens = tokenise(expression)
    parse_tree = parse(tokens)
    # An error occurred in parsing
    if parse_tree is None:
        return None

    return evaluate_parse_tree(parse_tree)


if __name__ == "__main__":
    # Given test cases
    tests = {
        "1 + 3": 4,
        "(1 + 3) * 2": 8,
        "(4 / 2) + 6": 8,
        "4 + (12 / (1 * 2))": 10,
        "(1 + (12 * 2)": None,
    }

    # Simple comparative testing
    for test in tests:
        result = evaluate(test)
        if result == tests[test]:
            print(f"GOOD {test}")
        else:
            print(f"BAD  {test}, {result}")


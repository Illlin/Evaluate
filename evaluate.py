from typing import Optional, List


def tokenise(expression: str, special_tokens="()+-*/") -> List[str]:
    """Returns a list of tokens"""
    # In the current grammar every special token is exactly 1 character long, and numbers can be any length
    # Read through string from left to right, building up tokens
    expression = expression.strip()  # We can ignore all white space

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


def parse(tokens: List[str]):
    pass


def evaluate_parse_tree(parse_tree) -> Optional[int]:
    pass


def evaluate(expression: str) -> Optional[int]:
    """Returns the result, or None if there was an error."""
    # The parsing and evaluation of the expression grammar will be split into 3 parts,
    # tokenisation, parsing, and evaluation
    tokens = tokenise(expression)
    parse_tree = parse(tokens)
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
        if result == tests[test]:  # Does not work with None
            print(f"GOOD {test}")
        else:
            print(f"BAD  {test}, {result}")


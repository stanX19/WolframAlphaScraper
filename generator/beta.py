import random
import logging


class VALID:
    VALUES = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    OPERATORS = ["+", "-", "/", 'e^']
    FUNCTIONS = ["sin", "cos", "tan"]  # , "exp", "log"]
    VARIABLES = ["x"]  # , "y", "z"]
    OPEN_BRACKET = ["("]
    CLOSE_BRACKET = [")"]
    ALL_TYPES = [VALUES, OPERATORS, FUNCTIONS, VARIABLES, OPEN_BRACKET, CLOSE_BRACKET]


ENUM_VALUES = 0
ENUM_OPERATORS = 1
ENUM_FUNCTIONS = 2
ENUM_VARIABLES = 3
ENUM_OPEN_BRACKET = 4
ENUM_CLOSE_BRACKET = 5


def add_to_pool(pool: list, *args):
    for i in args:
        pool[i] += 1


def beta_generate_expression(max_terms=10):
    nested = []
    in_function = 0
    expression = []

    # generate the first term of the expression
    chosen_type = random.choice([ENUM_VALUES, ENUM_VARIABLES, ENUM_FUNCTIONS])
    expression.append(random.choice(VALID.ALL_TYPES[chosen_type]))

    # generate the rest of the terms iteratively
    term_count = 0
    prev_type = chosen_type
    
    while term_count < max_terms or prev_type == ENUM_OPERATORS or prev_type == ENUM_OPEN_BRACKET\
            or prev_type == ENUM_FUNCTIONS:
        pool = [0, 0, 0, 0, 0, 0]
        # [VALID_VALUES, VALID_OPERATORS, VALID_FUNCTIONS, VALID_VARIABLES, OPEN_BRACKET, CLOSE_BRACKET]
        if nested and nested[-1] > 1:
            add_to_pool(pool, ENUM_CLOSE_BRACKET)

        # conditions
        if prev_type == ENUM_VALUES:
            add_to_pool(pool, ENUM_VALUES, ENUM_FUNCTIONS, ENUM_VARIABLES, ENUM_OPERATORS)
        elif prev_type == ENUM_FUNCTIONS:
            pool = [0, 0, 0, 0, 0, 0]
            pool[ENUM_OPEN_BRACKET] = 1
        elif prev_type == ENUM_OPERATORS:
            pool[ENUM_CLOSE_BRACKET] = 0
            add_to_pool(pool, ENUM_FUNCTIONS, ENUM_VALUES, ENUM_OPEN_BRACKET)
        elif prev_type == ENUM_VARIABLES:
            add_to_pool(pool, ENUM_OPERATORS, ENUM_FUNCTIONS, ENUM_OPEN_BRACKET)
        elif prev_type == ENUM_OPEN_BRACKET:
            pool = [0, 0, 0, 0, 0, 0]
            add_to_pool(pool, ENUM_FUNCTIONS, ENUM_VARIABLES)
        elif prev_type == ENUM_CLOSE_BRACKET:
            add_to_pool(pool, ENUM_FUNCTIONS, ENUM_OPERATORS)

        # special case
        if in_function:
            pool[ENUM_FUNCTIONS] = 0

        # choose
        chosen_type = random.choice([idx for idx, val in enumerate(pool) if val > 0])
        term = random.choice(VALID.ALL_TYPES[chosen_type])

        # record
        if term == '(':
            nested.append(0)
        elif term == ')':
            nested.pop(-1)
        elif nested:
            nested[-1] += 1
        if chosen_type == ENUM_FUNCTIONS:
            in_function += 1
        expression.append(term)
        prev_type = chosen_type

        term_count += 1

    for i in range(len(nested)):
        expression.append(')')
    # convert the expression into an integral expression and return it
    variable = random.choice(VALID.VARIABLES)
    return "".join(expression)


if __name__ == '__main__':
    print(beta_generate_expression(10))

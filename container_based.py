import random
import logging

ENUM_INTEGER = 1
ENUM_LINEAR = 2
ENUM_NON_LINEAR = 4
ENUM_ARITHMETIC = 8
ENUM_FUNCTIONS = 16
ENUM_CONTAINERS = 24
ENUM_ALL = 31

ARITHMETIC = {  # container: types of expressions
    "{}+{}": [ENUM_INTEGER, ENUM_ALL - ENUM_INTEGER - ENUM_ARITHMETIC],
    "{}+{}K": [ENUM_ALL - ENUM_INTEGER, ENUM_ALL - ENUM_INTEGER],
    "{}-{}": [ENUM_INTEGER, ENUM_ALL - ENUM_INTEGER - ENUM_ARITHMETIC],
    "{}-{}K": [ENUM_ALL - ENUM_INTEGER, ENUM_ALL - ENUM_INTEGER],
}

FUNCTIONS = {  # container: types of expressions
    "(({})e^({}))": [ENUM_ALL, ENUM_LINEAR],
    "(({})/({}))": [ENUM_ALL, ENUM_ALL - ENUM_INTEGER],
    "(1/({}))": [ENUM_ALL - ENUM_INTEGER],

    "(({})tan({}))": [ENUM_ALL, ENUM_LINEAR],
    "(({})sin({}))": [ENUM_ALL, ENUM_LINEAR],
    "(({})cos({}))": [ENUM_ALL, ENUM_LINEAR],

    "(({})tan({})^2)": [ENUM_ALL, ENUM_LINEAR],
    "(({})sin({})^2)": [ENUM_ALL, ENUM_LINEAR],
    "(({})cos({})^2)": [ENUM_ALL, ENUM_LINEAR],

    "(e^({}))": [ENUM_LINEAR + ENUM_NON_LINEAR],
    "(ln({}))": [ENUM_LINEAR + ENUM_NON_LINEAR],
    "(sqrt({}))": [ENUM_ALL - ENUM_INTEGER],

    "{}({})": [ENUM_NON_LINEAR + ENUM_LINEAR, ENUM_CONTAINERS]
}

CONTAINERS = {}
CONTAINERS.update(ARITHMETIC)
CONTAINERS.update(FUNCTIONS)
# K = dummy to separate keys, replace to '' later

EXP_DICT = {
    ENUM_INTEGER: {"{}": 1},
    ENUM_LINEAR: {"{}x": 1,
                  "x": 0,
                  "2x": 0},
    ENUM_NON_LINEAR: {"{}(x^({}))": 2,
                      "{}(x^(-{}))": 2,
                      "(x^({}))": 1,
                      "(x^(-{}))": 1}
}

_max_container = 0
_max_depth = 0


def _container_based(_constrain=ENUM_ALL, _depth=0):
    global _max_container

    if _depth == 0 and _max_container and (_constrain & ENUM_ARITHMETIC):  # priority
        _max_container -= 1
        container = random.choice(list(ARITHMETIC))
        child_args = ARITHMETIC[container]
        expression = container.format(*[_container_based(arg, _depth) for arg in child_args])
        return expression

    elif _depth < _max_depth and _max_container and (_constrain & ENUM_CONTAINERS):
        _max_container -= 1
        container = random.choice(list(CONTAINERS))
        child_args = CONTAINERS[container]
        expression = container.format(*[_container_based(arg, _depth + 1) for arg in child_args])
        return expression

    else:
        bit_range = 3
        options = [1 << i for i in range(bit_range) if ((1 << i) & _constrain)]
        try:
            choice = random.choice(options)
        except IndexError:  # restriction matches none
            return _container_based(_depth=_depth)  # no restriction

        expressions_dict = EXP_DICT[choice]
        expression, argc = random.choice(list(expressions_dict.items()))
        return expression.format(*[random.randint(2, 3) for arg in range(argc)])


def generate_expression(max_container=3, max_depth=2):
    global _max_container, _max_depth

    _max_container = max_container
    _max_depth = max_depth
    expression = _container_based().replace('K', '')

    logging.info(f"Expression generated: {expression}")
    return expression


def verify_containers():
    ok = True

    for key, val in CONTAINERS.items():
        bc = key.count(')')  # bracket close
        bo = key.count('(')  # bracket open
        rf = key.count('{}')  # replacement fields
        ac = len(val)  # arg count
        
        if bo != bc and rf != ac:
            print(f"Error: \"{key}\" \n    --> '(' = {bo}, ')' = {bc} \n    --> '{{}}'= {rf}, arg = {ac}")
            ok = False
        elif bo != bc:
            print(f"Error: \"{key}\" \n    --> '(' = {bo}, ')' = {bc}")
            ok = False
        elif rf != ac:
            print(f"Error: \"{key}\" \n    --> '{{}}'= {rf}, arg = {ac}")
            ok = False

    return ok


if __name__ == '__main__':
    if verify_containers():
        print(generate_expression(5))



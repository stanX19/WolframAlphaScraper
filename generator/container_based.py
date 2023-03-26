import random
import logging

ENUM_INTEGER = 1
ENUM_LINEAR = 2
ENUM_NON_LINEAR = 4
ENUM_CONTAINER = 8
ENUM_ALL = 15

CONTAINERS = {  # container: types of expressions
    "(({})e^({}))": [ENUM_ALL, 1 + 2 + 4],
    "(({})/({}))": [ENUM_ALL, ENUM_ALL - 1],
    "(({})tan({}))": [ENUM_ALL, ENUM_LINEAR],
    "(({})sin({}))": [ENUM_ALL, ENUM_LINEAR],
    "(({})cos({}))": [ENUM_ALL, ENUM_LINEAR],
    "(e^({}))": [ENUM_LINEAR + ENUM_NON_LINEAR],
    "{}+{}": [1, 15 - 1],
    "{}+{}K": [15 - 1, 15 - 1],
    "{}-{}": [1, 15 - 1],
    "{}-{}K": [15 - 1, 15 - 1],
    "{}({})": [ENUM_NON_LINEAR + ENUM_LINEAR, ENUM_ALL]
}
# K = dummy to separate keys, replace to '' later

EXP_DICT = {
    ENUM_INTEGER: {"{}": 1},
    ENUM_LINEAR: {"{}x": 1,
                  "x": 0},
    ENUM_NON_LINEAR: {"{}(x^({}))": 2,
                      "(x^({}))": 1}
}

_max_container = 0


def _container_based(_constrain=ENUM_ALL):
    global _max_container

    if _max_container and (_constrain & ENUM_CONTAINER):
        choice = ENUM_CONTAINER
    else:
        bit_range = 3
        options = [1 << i for i in range(bit_range) if ((1 << i) & _constrain)]
        choice = random.choice(options)

    if choice == ENUM_CONTAINER:
        _max_container -= 1
        container = random.choice(list(CONTAINERS))
        child_args = CONTAINERS[container]
        expression = container.format(*[_container_based(arg) for arg in child_args])
        return expression
    else:
        expressions_dict = EXP_DICT[choice]
        expression, argc = random.choice(list(expressions_dict.items()))
        return expression.format(*[random.randint(2, 9) for arg in range(argc)])


def generate_expression(max_container=3):
    global _max_container
    _max_container = max_container
    expression = _container_based().replace('K', '')

    logging.info(f"Expression generated: {expression}")
    return expression


def verify_containers():
    ok = True

    for key in CONTAINERS:
        if key.count('(') != key.count(')'):
            print(f"KO: {key}")
            ok = False
    return ok


if __name__ == '__main__':
    verify_containers()
    print(generate_expression(5))



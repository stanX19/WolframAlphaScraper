import random
import logging


class VALID:
    VALUES = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    OPERATORS = ["+", "-", "/", 'e^']
    FUNCTIONS = ["sin", "cos", "tan"]  # , "exp", "log"]
    VARIABLES = ["x"]  # , "y", "z"]
    OPEN_BRACKET = ["("]
    CLOSE_BRACKET = [")"]
    ALL = VALUES + OPERATORS + FUNCTIONS + VARIABLES + OPEN_BRACKET + CLOSE_BRACKET

expression_length = 10
mat = [[]]

def propagate():
    pass

def generate():
    global mat
    mat = [[True for i in ALL] for i in range(expression_length)]
    propagate()
    expression_list = [i.find(True) for i in mat]
    return ''.join(expression_list)

if __name__ == '__main__':
    print(generate())
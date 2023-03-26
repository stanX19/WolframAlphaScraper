import logging


def convert_to_integral(expression):
    integral_expression = "Integrate[" + expression + ", x]"
    return integral_expression

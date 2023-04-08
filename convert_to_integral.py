import random


def generate_low_high(expression: str):
    if 'sin' in expression or 'cos' in expression or 'tan' in expression:
        denominator = random.choice([2, 3, 4, 6, 12])
        low = random.randint(0, 2 * denominator)
        high = random.randint(1, denominator)*random.choice([1, -1])
        return [f'({low}/{denominator})pi', f'({high}/{denominator})pi']
    if 'e' in expression:
        low = random.randint(0, 3)
        high = low + random.randint(1, 3) * random.choice([1, -1])
        return [f'ln({low})', f'ln({high})']

    low = random.randint(0, 3)
    high = low + random.randint(1, 3) * random.choice([1, -1])
    return [low, high]


def indefinite_integral(expression):
    integral_expression = "Integrate[" + expression + ", x]"
    return integral_expression


def definite_integral(expression, low, high):
    integral_expression = f"Integrate[{expression}, [x, {low}, {high}]]"
    return integral_expression

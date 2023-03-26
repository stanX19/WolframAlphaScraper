import os
from generator import generate_expression, convert_to_integral
from scraper import scrape_solution_image
from write_img import write_img
import logging


def main():
    logging.basicConfig(level=logging.INFO)  # DEBUG INFO WARNING ERROR CRITICAL

    input("Press enter to execute")
    not_satisfied = "1"
    expression = ""
    while not_satisfied:
        expression = generate_expression(4)  # input("expression: ")  # 'D[(x^2)e^x,x]'
        not_satisfied = input()
    try:
        query = convert_to_integral(expression)
        img_data = scrape_solution_image(query, headless=True)
    except (TimeoutError, ValueError) as exc:
        logging.error(exc)
        return

    path = f"data\\{query}.png"
    try:
        write_img(path, img_data)
        os.startfile(path)
    except OSError:
        print(f"Img Data: {img_data}")


if __name__ == '__main__':
    while True:
        main()

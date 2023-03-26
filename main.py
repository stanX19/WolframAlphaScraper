import os
from generator import generate_expression, convert_to_integral
from scraper import scrape_solution_image
from write_img import write_img
import logging


def main():
    logging.basicConfig(level=logging.INFO)  # DEBUG INFO WARNING ERROR CRITICAL

    input("Press enter to execute")
    expression = generate_expression(2)  # input("expression: ")  # 'D[(x^2)e^x,x]'
    try:
        query = convert_to_integral(expression)
        img_data = scrape_solution_image(query, headless=False)
    except (TimeoutError, ValueError) as exc:
        logging.error(exc)
        return

    path = f"data\\{query}.png"
    try:
        write_img(path, img_data)
        os.startfile(path)
    except OSError as exc:
        logging.error(exc)
        logging.info(f"Img Data: {img_data}")


if __name__ == '__main__':
    while True:
        main()

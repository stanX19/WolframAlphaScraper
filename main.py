import os
import time
from generator import generate_expression, definite_integral, generate_low_high
from scraper import scrape_solution_image
from write_img import write_img
import logging


def run(directory: str, max_container: int, max_depth: int):
    expression = generate_expression(max_container, max_depth)  # input("expression: ")  # 'D[(x^2)e^x,x]'
    try:
        query = definite_integral(expression, *generate_low_high(expression))
        img_data = scrape_solution_image(query, headless=True)
    except (TimeoutError, ValueError) as exc:
        logging.error(exc)
        return

    date_time = time.strftime('%Y-%m-%d %H_%M_%S', time.localtime(time.time()))
    path = f"{directory}\\{date_time}.png"
    try:
        write_img(path, img_data)
    except OSError as exc:
        logging.error(exc)
    return path

def main():
    logging.basicConfig(level=logging.INFO)  # DEBUG INFO WARNING ERROR CRITICAL

    N = int(input("Loop count: "))
    directory = input("Base dir: ")
    max_container = int(input("Max container: "))
    max_depth = int(input("Max depth: "))

    if not os.path.exists(directory):
        logging.info(f"Created directory: {directory}")
        os.mkdir(directory)

    paths = []
    for i in range(N):
        path = run(directory, max_container, max_depth)
        if path:
            paths.append(path)
        logging.info("")
    for path in paths:
        os.startfile(path)


if __name__ == '__main__':
    main()

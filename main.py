import os
import time
import logging
from generator import generate_expression, definite_integral, generate_low_high
from scraper import scrape_solution_image
from write_img import write_img
from notify import notify_when_done, show_notification


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

    # Get input values
    N = int(input("Loop count: "))
    directory = os.path.join("saved_solutions", input("Base dir: "))
    max_container = int(input("Max container: "))
    max_depth = int(input("Max depth: "))

    # Measure execution time
    start_time = time.perf_counter()

    # Change working directory to the script's directory
    os.chdir(os.path.abspath(os.path.dirname(__file__)))

    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        logging.info(f"Created directory: {directory}")
        os.mkdir(directory)

    # Run the function N times and save successful paths
    paths = []
    try:
        for i in range(N):
            path = run(directory, max_container, max_depth)
            if path:
                paths.append(path)
            logging.info("")
    except Exception as exc:
        show_notification(exc, f"ERROR")
        raise exc

    # Notify user of completion and execution time
    notify_when_done(N, len(paths), round(time.perf_counter() - start_time, 2))

    # Open successful paths
    for path in paths:
        os.startfile(path)


if __name__ == '__main__':
    main()

import os
import time
import logging
import platform
import subprocess
from container_based import generate_expression
from convert_to_integral import definite_integral, generate_low_high
import scraper
from write_img import write_img
from notify import notify_when_done, show_notification


def run(directory: str, max_container: int, max_depth: int):
    expression = generate_expression(max_container, max_depth)  # input("expression: ")  # 'D[(x^2)e^x,x]'
    try:
        query = definite_integral(expression, *generate_low_high(expression))
        img_data = scraper.scrape_solution_image(query, headless=True)
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


def open_files(paths, success, directory):
    if success <= 5:
        for path in paths:
            if platform.system() == 'Windows':
                os.startfile(path)
            elif platform.system() == 'Linux':
                subprocess.Popen(['xdg-open', path])
    else:
        if platform.system() == 'Windows':
            os.startfile(directory)
        elif platform.system() == 'Linux':
            subprocess.Popen(['xdg-open', directory])


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
    success = 0
    try:
        for i in range(N):
            path = run(directory, max_container, max_depth)
            if path:
                if len(paths) < 5:
                    paths.append(path)
                success += 1
                logging.info(f"Status: SUCCESS | Loop no: {i + 1} | Total Success: {success}\n")
            else:
                logging.info(f"Status: TERMINATED | Loop no: {i + 1} | Total Success: {success}\n")
    except Exception as exc:
        show_notification(exc, f"ERROR")
        raise exc

    # terminate
    scraper.quit_browser()

    # Notify user of completion and execution time
    notify_when_done(N, success, round(time.perf_counter() - start_time, 2))

    # Open successful paths
    open_files(paths, success, directory)


if __name__ == '__main__':
    main()

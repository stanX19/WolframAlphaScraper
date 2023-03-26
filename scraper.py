import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import TimeoutException


def scrape_solution_image(expression: str, headless=True, wait_for=20, seek_error=True):
    # Set up options for headless browser
    options = Options()
    options.headless = headless

    # Create an instance of the WebDriver object
    browser = webdriver.Edge(options=options)
    logging.info("browser started")

    # Encode the query string
    encoded_query = requests.utils.quote(expression)

    # Construct the URL of the Wolfram Alpha page
    url = f'https://www.wolframalpha.com/input?i2d=true&i={encoded_query}'
    # Navigate to the Wolfram Alpha page
    logging.info(f"Visiting WolframAlpha...")
    logging.info(f"Url = {url}")
    browser.get(url)

    # Wait for the solution to appear
    logging.info("Waiting for the solution to appear...")

    # Look for the error message first
    try:
        # Look for either the error or solution element
        wait = WebDriverWait(browser, wait_for)
        if seek_error:
            XPATH = "//*[contains(@class,'_tc9a') or contains(@class,'_Xijx')]"
        else:
            XPATH = "contains(@class,'_Xijx')]"
        element = wait.until(EC.presence_of_element_located((By.XPATH, XPATH)))

        if element.get_attribute("class") == "_tc9a":
            error_text = element.find_element(By.TAG_NAME, "span").text
            raise ValueError(error_text)
        else:
            solution = element

    except TimeoutException:
        raise TimeoutError(f"Wolfram Alpha took too long to respond (>{wait_for}s)")

    image_src = solution.get_attribute('src')
    logging.info(f"Image source found: {image_src[:60]}...")

    browser.quit()

    # Extract img data from src
    try:
        return image_src.split(',')[1]
    except IndexError:
        raise ValueError("Incorrect url format, abort")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # DEBUG INFO WARNING ERROR CRITICAL

    expression = 'D[(x^2)e^x,x]'
    try:
        img_data = scrape_solution_image(expression, headless=False, wait_for=60)
    except (TimeoutError, ValueError) as exc:
        logging.error(exc)
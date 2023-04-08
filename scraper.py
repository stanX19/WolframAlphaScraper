import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import TimeoutException


browser = None


def quit_browser():
    global browser
    if isinstance(browser, webdriver.Edge):
        browser.quit()
        logging.info("browser terminated")
        browser = None


def scrape_solution_image(expression: str, headless=True, wait_for=20, definite=True):
    global browser

    # Set up options for headless browser
    options = Options()
    options.headless = headless

    # Create an instance of the WebDriver object
    if browser is None:
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
        # error text
        ERROR_TEXT = {
            "Wolfram|Alpha doesn't understand your query": ValueError,
            "Standard computation time exceeded...": TimeoutError,
        }

        # XPATH of various target
        ERROR_XPATH = " | ".join("//section//*[text()=\"{}\"]".format(t) for t in ERROR_TEXT)
        INDEF_XPATH = "//section[contains(header/h2/span/text(),\
                        'Indefinite integral')]/descendant::*//img[contains(@class,'_Xijx')]"
        DEFIN_XPATH = "//section[contains(header/h2/span/text(),\
                        'Definite integral')]/descendant::*//img[contains(@class,'_Xijx')]"

        if definite:
            XPATH = f"{ERROR_XPATH} | {DEFIN_XPATH}"
        else:
            XPATH = f"{ERROR_XPATH} | {INDEF_XPATH} | {DEFIN_XPATH}"
        # Look for either the error or solution element
        wait = WebDriverWait(browser, wait_for)
        element = wait.until(EC.presence_of_element_located((By.XPATH, XPATH)))

        if hasattr(element, "text") and element.text in ERROR_TEXT:
            raise ERROR_TEXT[element.text](element.text)

    except TimeoutException:
        raise TimeoutError(f"Wolfram Alpha took too long to respond (>{wait_for}s)")

    # at this point must have image, based on previous xpath
    image_src = element.get_attribute('src')
    logging.info(f"Image source found: {image_src[:60]}...")

    # Extract img data from src
    try:
        return image_src.split(',')[1]
    except IndexError:
        raise ValueError("Incorrect img src format, abort")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  # DEBUG INFO WARNING ERROR CRITICAL

    _expression = 'Integrate[(x^x)e^x, x]'
    try:
        img_data = scrape_solution_image(_expression, headless=False, wait_for=60)
    except (TimeoutError, ValueError) as exc:
        logging.error(exc)

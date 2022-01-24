from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.webelement import WebElement

GAME_URL = "https://www.powerlanguage.co.uk/wordle/"
WORDS_FILE = "words.txt"

def _get_words():
    with open(WORDS_FILE, 'r') as f:
        return f.read().splitlines()

def _enter_word(word: dict, root: WebElement) -> dict:
    return result

def get_driver(driver: str, headless: bool) -> webdriver:
    """Returns a driver class instance using the specified driver/options."""
    options = None
    if headless and driver == "Chrome":
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
    return getattr(webdriver, driver)(options=options)

def solver(driver: str, method: str, headless: bool) -> bool:
    """The main function to start selenium and solve the challenge."""
    words = _get_words()
    browser = get_driver(driver, headless)
    browser.get(GAME_URL)
    print(type(browser))
    #root.click()
    browser.quit()

if __name__ == '__main__':
    solver("Chrome", "fast", True)

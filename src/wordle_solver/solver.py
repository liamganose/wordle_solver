from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

GAME_URL = "https://www.powerlanguage.co.uk/wordle/"

def solver(driver: str, method: str, headless: bool) -> bool:
    """The main function to start selenium and solve the challenge."""
    browser = get_driver(driver, headless)
    browser.get(GAME_URL)
    root = browser.find_element_by_tag_name('html')
    root.click()
    browser.quit()

def get_driver(driver: str, headless: bool) -> webdriver:
    """Returns a driver class instance using the specified driver/options."""
    options = None
    if headless and driver == "Chrome":
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
    return getattr(webdriver, driver)(options=options)

def enter_word(word: dict, root: WebElement) -> dict:
    return result

if __name__ == '__main__':
    solver("Chrome", "fast", True)

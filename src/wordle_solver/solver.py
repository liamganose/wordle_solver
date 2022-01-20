from selenium import webdriver
from selenium.webdriver.common.keys import Keys

GAME_URL = "https://www.powerlanguage.co.uk/wordle/"

def solver(driver: str, method: str) -> bool:
    """The main function to start selenium and solve the challenge."""
    driver = getattr(webdriver, driver)()
    driver.get(GAME_URL)
    keyboard = driver.find_element_by_id("game-keyboard")
    board = driver.find_element_by_id("board")

if __name__ == "__main__":
    solver("Chrome", "fast")

import time
import re
import logging
from typing import List, Set, Tuple, NewType, Union

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

GAME_URL: str = "https://www.powerlanguage.co.uk/wordle/"
WORDS_FILE: str = "words.txt"
WordList = List[str]
Element = NewType("Element", webdriver.remote.webelement.WebElement)
ElementList = List[Element]

def _get_guess(word_data: dict, guesses: int, words: WordList) -> str:
    if guesses == 0:
        return "orate"
    
    # filter using correct letters
    reg_filter = [".", ".", ".", ".", "."]
    for index, letter in word_data["correct"].items():
        reg_filter[index] = letter
    reg_filter = re.compile("".join(reg_filter))
    words = list(filter(reg_filter.match, words))
    
    # filter on present letters
    for letter in word_data["present"]:
        words = list(filter(lambda word: letter in word, words))

    # inverse filter on absent letters
    for letter in word_data["absent"]:
        words = list(filter(lambda word: letter not in word, words))

    return words[0] 

def _get_board(browser: webdriver, element: Element) -> Element:
    script: str = 'return arguments[0].shadowRoot.getElementById("board")'
    return browser.execute_script(script, element)

def _get_tiles(browser: webdriver, row: Element) -> ElementList:
    script: str = 'return arguments[0].shadowRoot.querySelectorAll("game-tile")'
    return browser.execute_script(script, row)

def _get_words() -> WordList:
    with open(WORDS_FILE, 'r') as f:
        return f.read().splitlines()

def _run_game(browser: webdriver, root: Element, words: WordList) -> None:
    board: Element = _get_board(browser, browser.find_element(By.TAG_NAME, "game-app"))
    rows: ElementList = board.find_elements(By.TAG_NAME, "game-row")
    guesses: int = 0
    word_data: dict = {"correct": dict(), "present": set(), "absent": set()}
    while(True):
        time.sleep(1)
        word: str = _get_guess(word_data, guesses, words)
        row: Element = rows[guesses]
        guesses += 1
        logging.info(f"guess = {guesses}, word = {word}")
        root.send_keys(word)
        root.send_keys(Keys.ENTER)
        time.sleep(1)
        correct = 0
        for index, tile in enumerate(_get_tiles(browser, row)):
            evaluation: str = tile.get_attribute("evaluation")
            letter: str = tile.get_attribute("letter")
            if evaluation == "correct":
                correct += 1
                word_data[evaluation][index] = letter
            else:
                word_data[evaluation].add(letter)
        logging.info(word_data)
        if correct == 5:
            logging.info(f"Correct answer found in {guesses} guesses.")
            break
        if guesses == len(rows):
            logging.info("Ran out of guesses before getting the correct answer.")
            break

def get_driver(driver: str, headless: bool) -> webdriver:
    """Returns a driver class instance using the specified driver/options."""
    options: Union[None,webdriver] = None
    if headless and driver == "Chrome":
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
    return getattr(webdriver, driver)(options=options)

def solver(driver: str, headless: bool) -> bool:
    """The main function to start selenium and solve the challenge."""
    words: WordList = _get_words()
    browser: webdriver = get_driver(driver, headless)
    browser.get(GAME_URL)
    logging.info(f"Opened {GAME_URL}.")
    root: Element = browser.find_element(By.TAG_NAME, "html")
    root.click() # get rid of popup
    time.sleep(1)
    logging.info("Running game...")
    _run_game(browser, root, words)
    browser.quit()

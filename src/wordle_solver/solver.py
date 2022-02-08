import logging
import os
import re
import time
from typing import List, NewType, Union

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from definitions import ROOT_DIR

GAME_URL: str = "https://www.powerlanguage.co.uk/wordle/"
WORDS_FILE: str = os.path.join(ROOT_DIR, "words.txt")
WordList = List[str]
Element = NewType("Element", webdriver.remote.webelement.WebElement)
ElementList = List[Element]
LETTERS_ORDERED = [
    "e", "a", "r", "i", "o", "t", "n", "s", "l", "c", "u", "d", "p",
    "m", "h", "g", "b", "f", "y", "w", "k", "v", "x", "z", "j", "q"
]


def _get_guess(word_data: dict, guesses: int, words: WordList) -> Union[WordList, str]:
    """Given a word list, number of guesses and past guesses, return a new word."""
    if guesses == 0:
        return "crane"

    # filter for letters we know and definitely don't know
    reg_filter = ["", "", "", "", ""]
    for i in range(5):
        if i in word_data["correct"]:
            reg_filter[i] = word_data["correct"][i]
        elif i in word_data["present_position"]:
            reg_filter[
                i] = f"[^{(word_data['absent'] - word_data['present']) | set(word_data['present_position'][i])} ]"
        else:
            reg_filter[i] = f"[^{word_data['absent'] - word_data['present']}]"
    reg_filter = re.compile("".join(reg_filter))
    logging.info(f"{reg_filter=}")
    words = list(filter(reg_filter.match, words))
    logging.info(f"After filter left {len(words)} words: {words}")

    # filter on present letters
    for letter in word_data["present"]:
        words = list(filter(lambda word: letter in word, words))

    # filter double letters
    dbl_letters: set = word_data["absent"] & word_data["present"]

    def _count_dbls(word):
        for letter in dbl_letters:
            if word.count(letter) > 1:
                return False
        return True

    words = list(filter(_count_dbls, words))

    # remove past guesses from the list
    words = list(filter(lambda word: word not in word_data["guesses"], words))

    # sort list by frequency rankings
    def _rank_function(word):
        return sum(LETTERS_ORDERED.index(word[i]) for i in range(5))

    words = sorted(words, key=_rank_function)

    return words


def _get_board(browser: webdriver, element: Element) -> Element:
    """Get the board from within the shadow root of the HTML."""
    script: str = 'return arguments[0].shadowRoot.getElementById("board")'
    return browser.execute_script(script, element)


def _get_tiles(browser: webdriver, row: Element) -> ElementList:
    """Get the tiles from within the given row element."""
    script: str = 'return arguments[0].shadowRoot.querySelectorAll("game-tile")'
    return browser.execute_script(script, row)


def _get_words() -> WordList:
    """Get the list of words from the words file."""
    with open(WORDS_FILE, 'r') as f:
        return f.read().splitlines()


def _run_game(browser: webdriver, root: Element, words: WordList) -> None:
    """Loop through the rows and make a guess."""
    board: Element = _get_board(browser, browser.find_element(By.TAG_NAME, "game-app"))
    rows: ElementList = board.find_elements(By.TAG_NAME, "game-row")
    guesses: int = 0
    word_data: dict = {"correct": dict(), "present_position": dict(), "present": set(),
                       "absent": set(), "guesses": set()}
    while True:
        time.sleep(1)
        if guesses > 0:
            words: WordList = _get_guess(word_data, guesses, words)
            word: str = words[0]
        else:
            word: str = _get_guess(word_data, guesses, words)
        word_data["guesses"].add(word)
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
                word_data["correct"][index] = letter
                word_data["present"] = word_data["present"] - {letter}
            elif evaluation == "present":
                word_data["present_position"][index] = letter
                word_data[evaluation].add(letter)
            else:
                word_data[evaluation].add(letter)
        logging.info(word_data)
        if correct == 5:
            logging.info(f"Correct answer: '{word}', found in {guesses} guesses.")
            break
        if guesses == len(rows):
            logging.info("Ran out of guesses before getting the correct answer.")
            break


def get_driver(driver: str, headless: bool) -> webdriver:
    """Returns a driver class instance using the specified driver/options."""
    options: Union[None, webdriver] = None
    if headless and driver == "Chrome":
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
    return getattr(webdriver, driver)(options=options)


def solver(driver: str, headless: bool) -> None:
    """The main function to start selenium and solve the challenge."""
    words: WordList = _get_words()
    browser: webdriver = get_driver(driver, headless)
    browser.get(GAME_URL)
    logging.info(f"Opened {GAME_URL}.")
    driver_wait = WebDriverWait(browser, 30)
    _ = driver_wait.until(ec.presence_of_element_located((By.TAG_NAME, "game-app")))
    root: Element = browser.find_element(By.TAG_NAME, "html")
    root.click()  # get rid of popup
    time.sleep(1)
    logging.info("Running game...")
    try:
        _run_game(browser, root, words)
    finally:
        # leave the window open for a while after the game finishes
        time.sleep(5)
        browser.quit()

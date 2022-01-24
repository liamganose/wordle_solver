import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from src.wordle_solver.solver import solver, get_driver

class DriverError(Exception):
    pass

@pytest.mark.drivertest
def test_driver_present(pytestconfig) -> None:
    driver: bool = pytestconfig.getoption('driver')
    headless: bool = pytestconfig.getoption('headless')
    try:
        d: webdriver = get_driver(driver, headless)
    except AttributeError:
        raise(DriverError(f"{driver} is not a valid web driver."))

@pytest.mark.maintest
def test_solver(pytestconfig):
    driver: bool = pytestconfig.getoption('driver')
    headless: bool = pytestconfig.getoption('headless')
    solver(driver, headless)

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import pytest
from src.wordle_solver.solver import solver, get_driver

class DriverError(Exception):
    pass

@pytest.mark.drivertest
def test_driver_present(pytestconfig):
    driver = pytestconfig.getoption('driver')
    headless = pytestconfig.getoption('headless')
    try:
        d = get_driver(driver, headless)
    except AttributeError:
        raise(DriverError(f"{driver} is not a valid web driver."))

def test_solver(pytestconfig):
    driver = pytestconfig.getoption('driver')
    test_driver_present(pytestconfig)

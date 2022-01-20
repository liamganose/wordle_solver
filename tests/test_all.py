from selenium import webdriver
import pytest
from src.wordle_solver.solver import solver

class DriverError(Exception):
    pass

@pytest.mark.drivertest
def test_driver_present(pytestconfig):
    driver = pytestconfig.getoption('driver')
    try:
        d = getattr(webdriver, driver)
    except AttributeError as e:
        raise(DriverError(f"{driver} is not a valid web driver."))

def test_solver(pytestconfig):
    driver = pytestconfig.getoption('driver')
    test_driver_present(pytestconfig)
    assert(solver(driver, 'accurate') == True)
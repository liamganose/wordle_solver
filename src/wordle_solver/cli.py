import click
import pytest
import logging

from src.wordle_solver.solver import solver
from definitions import TEST_DIR

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

@click.group()
def wordle() -> None:
    pass

@wordle.command()
@click.option('--driver', '-d', default='Chrome',
              show_default=True, type=str,
              help='the name of the Selenium driver to use.')
@click.option('--headless', '-h', default=False,
              show_default=True, is_flag=True, type=bool,
              help='whether or not to run Selenium without gui. (only works with chrome)')
def solve(driver: str, headless: bool) -> None:
    logger.info(f"Running wordle solver on {driver}.")
    solver(driver.title(), headless)

@wordle.command()
@click.option('--driver', '-d', default='Chrome',
              show_default=True, type=str,
              help='the name of the Selenium driver to use.')
@click.option('--just-drivers', '-d', default=False, show_default=True,
              is_flag=True, type=bool,
              help='whether to just test the Selenium driver is working.')
@click.option('--headless', '-h', default=False,
              show_default=True, is_flag=True, type=bool,
              help='whether or not to run Selenium without gui. (only works with chrome)')
def test(driver: str, just_drivers: bool, headless: bool) -> None:
    args = ['-v', '-x', TEST_DIR, '--driver', driver.title()]
    if just_drivers:
        args += ['-m', 'drivertest']
    if headless:
        args += ['--headless', 'True']
    logger.info(f"Running tests...")
    pytest.main(args)

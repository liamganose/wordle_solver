import click
import pytest
from src.wordle_solver.solver import solver

@click.group()
def wordle():
    pass

@wordle.command()
@click.option('--driver', '-d', default='Chrome',
              show_default=True, type=str,
              help='the name of the Selenium driver to use.')
@click.option('--method', '-m', default='accurate',
              show_default=True,
              type=click.Choice(['fast', 'accurate']),
              help='the name of the Selenium driver to use.')
def solve(driver: str, method: str):
    click.echo(f"Running {method} Wordle solver on {driver}.")
    solver(driver.title(), method)

@wordle.command()
@click.option('--driver', '-d', default='Chrome',
              show_default=True, type=str,
              help='the name of the Selenium driver to use.')
@click.option('--just-drivers', '-d', default=False, show_default=True,
              is_flag=True, type=bool,
              help='whether to just test the Selenium driver is working.')
def test(driver: str, just_drivers: bool):
    args = ['-v', '-x', 'tests', '--driver', driver.title()]
    if just_drivers:
        click.echo(f"Running driver tests.")
        pytest.main(args + ['-m', 'drivertest'])
    else:
        click.echo(f"Running all tests.")
        pytest.main(args)
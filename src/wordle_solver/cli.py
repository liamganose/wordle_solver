import click
from solver import solver

@click.command()
@click.option('--driver', '-d', default='Chrome',
              show_default=True, case_sensitive=False, type=str,
              help='the name of the Selenium driver to use.')
@click.option('--method', '-m', default='accurate',
              show_default=True, case_sensitive=False,
              type=click.Choice(['fast', 'accurate']),
              help='the name of the Selenium driver to use.')
def solve(driver: str, method: str):
    """This is an example script to learn Click."""
    click.echo(f"Running {method} Wordle solver on {driver}.")
    solver(driver, method)

##test
# - word list test
# - logic test
# - internet test
# - driver test
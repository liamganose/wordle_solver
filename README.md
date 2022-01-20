### Info
Basic Selenium bot to automatically solve the daily wordle challenge.

### Installation
1. Download and install Python3.
2. Clone this repo and `cd` into the wordle_solver directory.
3. Run `pip install .` or `pip install ".[test]"` to install the test suite.
4. Download the Selenium driver of your choice (https://selenium-python.readthedocs.io/installation.html#drivers).
5. Make sure the driver location is in your PATH.

### Running
1. To use the solver you should be in the root directory and run `wordle solve`.
2. The default driver is set to Chrome but if you want to switch use the `--driver` (-d) flag. E.G.:
    - `wordle solve --driver Firefox`
3. There are two solving methods available: `fast` and `accurate`. Accessed using the `--method` (-f) flag.
    - `fast` will attempt to solve it in fewer moves but has higher failure rate.
    - `accurate` will always get the correct answer but will not optimise attempts.

### Testing
1. Make sure you've installed wordle_solver with the test suites.
2. Run `wordle test`.
3. If you just want to check you've added the drivers correctly you can run `wordle test --just-drivers`

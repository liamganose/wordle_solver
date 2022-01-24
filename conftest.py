def pytest_addoption(parser) -> None:
    parser.addoption('--driver', action='store', default='Chrome')
    parser.addoption('--headless', action='store', default=False)

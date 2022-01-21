def pytest_addoption(parser):
    parser.addoption('--driver', action='store', default='Chrome')
    parser.addoption('--headless', action='store', default=False)

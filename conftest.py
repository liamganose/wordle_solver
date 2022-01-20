def pytest_addoption(parser):
    parser.addoption('--driver', action='store', default='Chrome')
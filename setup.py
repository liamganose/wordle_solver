import os
from setuptools import setup, find_packages

def read(fname: str) -> str:
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def require(fname: str) -> list[str]:
    return open(os.path.join(os.path.dirname(__file__), fname)).read().splitlines()

setup(
    name = "wordle_solver",
    version = "0.0.2",
    author = "Liam Ganose",
    author_email = "lganose@gmail.com",
    description = "Automatically solve the daily wordle challenge.",
    license = "BSD",
    url = 'https://github.com/liamganose/wordle_solver',
    keywords = "wordle solver bot",
    packages = find_packages(),
    install_requires=require('requirements.txt'),
    long_description=read('README.md'),
    entry_points={
        'console_scripts': [
            'wordle = src.wordle_solver.cli:wordle'
        ],
    },
)

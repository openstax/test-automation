import pytest

def pytest_addoption(parser):
    parser.addoption('--testall', action='store_true', help='Run all tests')

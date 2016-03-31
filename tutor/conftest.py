"""Add command option for parameterization."""


import pytest  # NOQA


def pytest_addoption(parser):
    """Add branch parameter."""
    parser.addoption('--testall', action='store_true', help='Run all tests')

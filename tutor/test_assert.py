"""Jenkins-CI test file."""


import pytest


slow = pytest.mark.skipif(
    not pytest.config.getoption('--testall'),
    reason='Ignoring slow or incomplete tests; use --testall for a full suite'
)


def f():
    """Simple return for testing."""
    return 3


def test_number():
    """Basic True test."""
    assert f() == 3


@slow
def test_function():
    """Parameter False test."""
    assert f() == 4

import pytest

slow = pytest.mark.skipif(
	not pytest.config.getoption('--testall'),
	reason='Ignoring slow or incomplete tests; use --testall for a full suite'
)

def f():
	return 3

def test_number():
	assert f() == 3

@slow
def test_function():
	assert f() == 4

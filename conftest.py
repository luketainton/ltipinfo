import pytest


@pytest.fixture(scope='session')
def ip():
    ip_value = "1.1.1.1"
    return ip_value

import pytest


@pytest.fixture(scope='session')
def ip():
    ip_value = "1.1.1.1"
    return ip_value

@pytest.fixture(scope='session')
def fqdn():
    fqdn_value = "one.one.one.one"
    return fqdn_value

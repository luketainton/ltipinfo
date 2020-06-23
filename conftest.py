import pytest


@pytest.fixture(scope='session')
def query():
    value = "one.one.one.one"
    return value


@pytest.fixture(scope='session')
def ip():
    ip_value = "1.1.1.1"
    return ip_value


@pytest.fixture(scope='session')
def privip():
    ip_value = "192.168.0.1"
    return ip_value


@pytest.fixture(scope='session')
def fqdn():
    fqdn_value = "one.one.one.one"
    return fqdn_value


@pytest.fixture(scope='session')
def subnets():
    subnets_value = "3.3.3.3/32\n2.2.2.2/32\n1.1.1.1/32\n"
    return subnets_value

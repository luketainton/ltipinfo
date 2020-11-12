#!/usr/bin/env python3
import main
import json


def test_get_true_ip_fqdn(query):
    """Ensure that the function returns an IP address."""
    test = main.get_true_ip(query)
    assert test == ["1.1.1.1", 1] or ["1.0.0.1", 1]


def test_get_true_ip_ip(ip):
    """Ensure that the function returns an IP address."""
    test = main.get_true_ip(ip)
    assert test == ["1.1.1.1", 0]


def test_get_my_ip():
    """Make sure an object is returned when the function is called."""
    test = main.get_my_ip()
    assert test is not None


def test_resolve_fqdn(fqdn):
    """Test resolving an FQDN."""
    ip = main.resolve_fqdn(fqdn)
    assert ip == "1.1.1.1" or "1.0.0.1"


def test_resolve_ptr(ip):
    """Test resolving a PTR."""
    ptr = main.resolve_ptr(ip)
    assert ptr == "one.one.one.one"


def test_is_address_private(privip):
    """Test if a private address can be identified."""
    test = main.is_address_private(privip)
    assert test == True


def test_get_ip_information(ip):
    """Ensure that the API returns correct information."""
    ip_info = json.loads(main.get_ip_information(ip))
    assert ip_info['country'] == "Australia"
    assert ip_info['city'] == "South Brisbane"
    assert ip_info['isp'] == "Cloudflare, Inc"
    bgp_as = ip_info['as'].split(" ")[0]
    assert bgp_as == "AS13335"


def test_get_as_subnets():
    """Ensure the API is querying the correct AS."""
    # AS13335 taken from above test
    resp = main.get_as_subnets("AS13335")
    assert "162.158.112.0/24" in resp


def test_sort_as_subnets(subnets):
    """Ensure that subnets are sorted correctly."""
    test = main.sort_as_subnets(subnets)
    assert test == ["1.1.1.1/32", "2.2.2.2/32", "3.3.3.3/32"]

#!/usr/bin/env python3
import main
import json


bgp_as = ""


def test_get_external_ip(ip):
    test = main.get_external_ip(ip)
    assert test is not None


def test_get_ip_information(ip):
    global bgp_as
    ip_info = json.loads(main.get_ip_information(ip))
    assert ip_info['country'] == "Australia"
    assert ip_info['city'] == "Sydney"
    assert ip_info['isp'] == "Cloudflare, Inc."
    bgp_as = ip_info['as'].split(" ")[0]
    assert bgp_as == "AS13335"


def test_get_as_subnets():
    global bgp_as
    resp = main.get_as_subnets(bgp_as)
    assert "162.158.112.0/24" in resp

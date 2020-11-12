#!/usr/bin/env python3


from requests import get
import json
import argparse
from ipaddress import ip_address, ip_network
import socket


def parse_args():
    """Parse arguments from command line."""
    parser = argparse.ArgumentParser(
        description="""This script gets information about a specified IP address or domain name.
        If an IP address is specified, a reverse lookup will attempt to find an associated
        domain name."""
    )
    parser.add_argument(
        "QUERY",
        help="Query item. Specify 'me', an IP address, or a domain name."
    )
    parser.add_argument(
        "-p",
        "--prefixes",
        dest='prefixes',
        action='store_true',
        help="Get IPv4 prefixes advertised by AS."
    )
    return parser.parse_args()


def get_true_ip(query):
    """Return IP address from query."""
    try:
        ip_address(query)
        my_ip = query
        fqdn_used = 0
    except ValueError:
        """Not a valid IPv4 Address"""
        if query == 'me':
            my_ip = get_my_ip()
            fqdn_used = 0
        else:
            my_ip = socket.gethostbyname(query)
            fqdn_used = 1
    return [my_ip, fqdn_used]


def get_my_ip():
    """If an IP address is not specified on the CLI, get the user's public IP."""
    ip = get('https://api.ipify.org').text
    return ip


def resolve_fqdn(fqdn):
    """Resolve the IP address of the specified FQDN."""
    ip = socket.gethostbyname(fqdn)
    return ip


def resolve_ptr(ip):
    """Resolve the PTR record from the IP address."""
    ptr = socket.gethostbyaddr(ip)[0]
    return ptr


def is_address_private(ip):
    """Return True if given address is in an RFC1918 range."""
    if ip_address(ip).is_private:
        return True


def get_ip_information(ip):
    """Get information about IP address."""
    info = get(f'http://ip-api.com/json/{ip}')
    return info.text


def get_as_subnets(bgp_as):
    """Get the subnets advertised by the IP's Autonomous System"""
    r = get(f"https://api.hackertarget.com/aslookup/?q={bgp_as}").text
    subnets = r.split('"')[4].split("\n", 1)[1]
    return subnets


def sort_as_subnets(subnets):
    """Sort the list of advertised prefixes in ascending order."""
    returned_list = []
    subnets = subnets.split()
    ips = sorted(ip_network(subnet) for subnet in subnets)
    for ip in ips:
        returned_list.append(str(ip))
    return returned_list


def main():
    """Run script."""

    header = "------------------------------\n"
    header += "|   IP Address Information   |\n"
    header += "|         Lookup Tool        |\n"
    header += "|                            |\n"
    header += "|     By Luke D. Tainton     |\n"
    header += "|        @luketainton        |\n"
    header += "------------------------------\n"
    print(header)

    args = parse_args()
    ip_data = get_true_ip(args.QUERY)
    my_ip = ip_data[0]
    fqdn_used = ip_data[1]

    if is_address_private(my_ip):
        print(f"ERROR: The IP address {my_ip} is private and cannot be queried.")
        exit()

    if not fqdn_used:
        try:
            my_ptr = resolve_ptr(my_ip)
        except socket.herror:
            my_ptr = "<NONE>"
    else: 
        my_ptr = args.QUERY

    my_info = json.loads(get_ip_information(my_ip))

    if my_info['status'] == "success":
        location = f"{my_info['country']}/{my_info['regionName']}/{my_info['city']}"
        timezone = my_info['timezone']
        isp = my_info['isp']
        bgp_as = my_info['as'].split(" ")[0]

        output = ""
        output += f"IP Address:           {my_ip}\n"
        output += f"Domain Name:          {my_ptr}\n"
        output += f"Location:             {location}\n"
        output += f"Timezone:             {timezone}\n"
        output += f"ISP:                  {isp}\n"
        output += f"Autonomous System:    {bgp_as}\n"

        print(output)

        if args.prefixes:
            print(f"\nIPv4 prefixes advertised by {bgp_as}:")
            subnets_ipv4 = get_as_subnets(bgp_as)
            sorted_subnets = sort_as_subnets(subnets_ipv4)
            for s in sorted_subnets:
                print(s)

    else:
        print("The query failed. Please try again.")


if __name__ == "__main__":
    main()

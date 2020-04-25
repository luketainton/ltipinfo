#!/usr/bin/env python3


from requests import get
import json
import argparse
from datetime import datetime
import ipaddress
import socket


def parse_args():
    """Parse arguments from command line."""
    parser = argparse.ArgumentParser(
        description="This script gets IP address information."
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
    parser.add_argument(
        "-o",
        "--output",
        dest='output',
        action='store_true',
        help="Write output of script to a file."
    )
    return parser.parse_args()


def get_my_ip():
    """If an IP address is not specified on the CLI, get the user's public IP."""
    ip = get('https://api.ipify.org').text
    return ip


def resolve_fqdn(fqdn):
    """Resolve the IP address of the specified FQDN."""
    ip = socket.gethostbyname(fqdn)
    return ip


def get_ip_information(ip):
    """Get information about IP address."""
    info = get(f'http://ip-api.com/json/{ip}')
    return info.text


def get_as_subnets(bgp_as):
    """Get the subnets advertised by the IP's Autonomous System"""
    r = get(f"https://api.hackertarget.com/aslookup/?q={bgp_as}").text
    return r.split('"')[4].split("\n", 1)[1]


def main():
    """Run script."""
    header = """
------------------------------
|   IP Address Information   |
|         Lookup Tool        |
|                            |
|     By Luke D. Tainton     |
|        @luketainton        |
------------------------------
    """

    print(header)
    args = parse_args()
    try:
        ipaddress.ip_address(args.QUERY)
        my_ip = args.QUERY
        fqdn_used = 0
    except ValueError:
        """Not a valid IPv4 Address"""
        if args.QUERY == 'me':
            my_ip = get_my_ip()
            fqdn_used = 0
        else:
            fqdn_used = 1
            my_ip = socket.gethostbyname(args.QUERY)
    my_info = json.loads(get_ip_information(my_ip))
    if my_info['status'] == "success":
        location = f"{my_info['country']}/{my_info['regionName']}/{my_info['city']}"
        timezone = my_info['timezone']
        isp = my_info['isp']
        bgp_as = my_info['as'].split(" ")[0]
        subnets_ipv4 = get_as_subnets(bgp_as)
        output = f"IP Address:           {my_ip}"
        if fqdn_used:
            output += f"\nDomain Name:          {args.QUERY}"
        output += f"""
Location:             {location}
Timezone:             {timezone}
ISP:                  {isp}
Autonomous System:    {bgp_as}
"""
        if args.prefixes:
            output += f"""

IPv4 prefixes advertised by {bgp_as}:
{subnets_ipv4}

Get more information at https://bgp.he.net/{bgp_as}.
        """

        if args.output:
            current_time = datetime.now().strftime('%Y%m%d-%H%M%S')
            filename = f"output-{current_time}.txt"
            with open(str(filename), 'w') as file:
                file.write(header)
                file.write(output)
                file.close()
            print(f"Output has been written to {filename}.")
        else:
            print(output)
    else:
        print("The query failed. Please try again.")


if __name__ == "__main__":
    main()

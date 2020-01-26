#!/usr/bin/env python3


from requests import get
import json
import argparse
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="This script gets IP address information.")
    parser.add_argument("ip", help="IP Address. Specify 'me' or an IP address.")
    parser.add_argument("-o", "--output", dest='output', action='store_true', help="Write output of script to a file.")
    return parser.parse_args()


def get_external_ip(args):
    if args.ip == 'me':
        ip = get('https://api.ipify.org').text
    else:
        ip = args.ip
    return ip


def get_ip_information(ip):
    info = get(f'http://ip-api.com/json/{ip}')
    return info.text


def get_as_subnets(bgp_as):
    r = get(f"https://api.hackertarget.com/aslookup/?q={bgp_as}").text
    return r.split('"')[4].split("\n", 1)[1]


def main():
    print("""
------------------------------
|   IP Address Information   |
|         Lookup Tool        |
|                            |
|     By Luke D. Tainton     |
|        @luketainton        |
------------------------------
    """)

    args = parse_args()
    my_ip = get_external_ip(args)
    my_info_raw = get_ip_information(my_ip)
    my_info = json.loads(my_info_raw)
    if my_info['status'] == "success":
        location = f"{my_info['country']}/{my_info['regionName']}/{my_info['city']}"
        timezone = my_info['timezone']
        isp = my_info['isp']
        bgp_as = my_info['as'].split(" ")[0]
        subnets_ipv4 = get_as_subnets(bgp_as)
        output = f"""
IP Address:           {my_ip}
Location:             {location}
Timezone:             {timezone}
ISP:                  {isp}
Autonomous System:    {bgp_as}

IPv4 prefixes advertised by {bgp_as}:
{subnets_ipv4}

Get more information at https://bgp.he.net/{bgp_as}.
        """

        if args.output:
            current_time = datetime.now().strftime('%Y%m%d-%H%M%S')
            filename = f"output-{current_time}.txt"
            with open(str(filename), 'w') as file:
                file.write(output)
                file.close()
            print(f"Output has been written to {filename}.")
        else:
            print(output)
    else:
        print("The query failed. Please try again.")


if __name__ == "__main__":
    main()

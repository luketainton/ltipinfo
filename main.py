#!/usr/bin/env python3


from requests import get
import json
import argparse


def parse_args():
	parser = argparse.ArgumentParser(description="This script gets IP address information.")
	parser.add_argument("ip", help="IP Address. Specify 'me' or an IP address.")
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
		subnets = get_as_subnets(bgp_as)

		print(f"""
IP Address:		{my_ip}
Location:		{location}
Timezone:		{timezone}
ISP:			{isp}
Autonomous System:	{bgp_as}

Prefixes advertised by {bgp_as}:
{subnets}
		""")

	else:
		print("The query failed. Please try again.")


if __name__ == "__main__":
    main()

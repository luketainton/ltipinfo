# IP Information Lookup Tool
This Python script takes an IP address and gathers information on the following:
- Location
- Timezone
- Internet Service Provider
- Autonomous System
- Advertised Prefixes

## Running the script
Running the script is easy. Just execute `./main.py me` to run against your own IP, or `./main.py <IPv4 ADDRESS>` to run against a specified IPv4 address.

## Credits
This script runs thanks to the APIs provided by [IP-API](http://ip-api.com) and [HackerTarget](https://hackertarget.com/as-ip-lookup). Thanks also to [Hurricane Electric](https://bgp.he.net) for providing
extra information on AS numbers.

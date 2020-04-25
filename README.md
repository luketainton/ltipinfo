# IP Information Lookup Tool

[![Total alerts](https://img.shields.io/lgtm/alerts/g/luketainton/ipinfo.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/luketainton/ipinfo/alerts)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/luketainton/ipinfo.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/luketainton/ipinfo/context:python)

This Python script takes an IP address or domain name and gathers the following information:
- Location
- Timezone
- Internet Service Provider
- Autonomous System
- Advertised Prefixes

## Running the script
Here are some ways that you can run the script:
| Command                | Description                              |
| ---------------------- | ---------------------------------------- |
| `./main.py me`         | Run against your own connection          |
| `./main.py 1.1.1.1`    | Run against the IP address `1.1.1.1`     |
| `./main.py google.com` | Run against the domain name `google.com` |

## Credits
This script runs thanks to the APIs provided by [IP-API](http://ip-api.com) and [HackerTarget](https://hackertarget.com/as-ip-lookup). Thanks also to [Hurricane Electric](https://bgp.he.net) for providing
extra information on AS numbers.

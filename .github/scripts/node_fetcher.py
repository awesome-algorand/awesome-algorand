import dns.resolver
import random
import requests
import json
from time import sleep

FILE_PATH = "relay_nodes.json"


def get_geo_data(ip):
    while True:
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            geo = response.json()
            return {
                "lat": geo["lat"],
                "lon": geo["lon"],
                "countryCode": geo["countryCode"],
                "country": geo["country"],
                "city": geo["city"],
            }
        except:
            print(f"Failed to fetch for {ip} retrying in 70 seconds")
            sleep(70)  # retry after 1 minute and 10 seconds
            continue


def get_ips():
    ips = []
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ["8.8.8.8"]  # use Google's DNS server

    try:
        answers = resolver.query("_algobootstrap._tcp.mainnet.algorand.network", "SRV")
    except dns.resolver.NoAnswer:
        return []

    for rdata in answers:
        print(f"Fetching for {rdata}")

        domain = rdata.target.to_text()
        try:
            answers = resolver.query(domain, "A")
        except:
            print(f"Failed to fetch for {domain}")
            continue

        record = random.choice(answers).to_text()
        try:
            geo_data = get_geo_data(record)
            ips.append({**geo_data, "domain": domain, "ip": record})
        except:
            print(f"Failed to fetch for {record}")
            continue

    return ips


ips = get_ips()

with open(FILE_PATH, "w") as f:
    json.dump(ips, f, indent=2)
    print(f"Saved {len(ips)} relay node metadata to {FILE_PATH}")

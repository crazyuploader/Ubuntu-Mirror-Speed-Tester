#!/usr/bin/env python3
"""Ubuntu Mirror Speed Tester"""


import csv
import shlex
import subprocess
import sys
from urllib.parse import urlparse
try:
    import requests
    import jc
    from tabulate import tabulate
except ImportError:
    print("Please run: pipenv install")
    sys.exit(1)


# Global Varaible(s)
HEADER = ["Hostname", "Full URL",
          "Average Latency (ms)", "Packet Loss (%)", "Download Speed (Bytes)", "Download Speed"]


# Function to write CSV
def write_to_csv(results, filename, header):
    """
    Function to write CSV
    """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for result in results:
            writer.writerow(result)


# Function to return human readable size from bytes
def sizeof_fmt(num, suffix="B/s"):
    """
    Function to return human readable size from bytes.
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


# Try to retrieve the mirrors list from the specified URL
MIRROR_URL = "http://mirrors.ubuntu.com/mirrors.txt"
try:
    print("Getting Mirrors List from:", MIRROR_URL)
    response = requests.get(MIRROR_URL, timeout=10)
    if response.status_code != 200:
        print("Getting mirrors list failed")
        sys.exit(1)
    mirrors = response.text.splitlines()
    print("Received mirrors list successfully")
    print("")
except requests.exceptions.RequestException as e:
    print("An error occurred while getting the mirrors list:")
    print(e)
    sys.exit(1)

# Iterate through the mirrors and perform the pings and downloads
mirror_results = []
for mirror in mirrors:
    hostname = urlparse(mirror).hostname
    full_url = mirror + "dists/jammy/Contents-amd64.gz"
    command = "curl -qfsLS -w '%{speed_download}' -o /dev/null --url" + " " + full_url
    curl_command = shlex.split(command)
    ping_command = shlex.split(f"ping -c 3 {hostname}")
    try:
        # Try to run the curl command and capture the output
        curl_speed_in_bytes = subprocess.run(
            curl_command, capture_output=True, check=True).stdout.decode("utf-8")
    except subprocess.CalledProcessError:
        print(
            f"An error occurred while running the curl command on mirror {hostname}")
        continue
    ICMP_CHECK = False
    try:
        # Try to ping the mirror and capture the output
        ping_output = subprocess.run(
            ping_command, capture_output=True, check=True).stdout.decode("utf-8")
        ICMP_CHECK = True
    except subprocess.CalledProcessError:
        print(f"An error occurred while pinging mirror {hostname}")
    if ICMP_CHECK is True:
        parsed_ping_output = jc.parse("ping", ping_output)
        AVERAGE_PING = f'{parsed_ping_output["round_trip_ms_avg"]} ms'
        PACKET_LOSS = f'{parsed_ping_output["packet_loss_percent"]}%'
    else:
        AVERAGE_PING = "na"
        PACKET_LOSS = "na"
    RESULT = [hostname, full_url, AVERAGE_PING, PACKET_LOSS,
        curl_speed_in_bytes, sizeof_fmt(float(curl_speed_in_bytes))]
    mirror_results.append(RESULT)


if mirror_results:
    write_to_csv(mirror_results, "result.csv", HEADER)
    print("")
    print(tabulate(mirror_results, HEADER))

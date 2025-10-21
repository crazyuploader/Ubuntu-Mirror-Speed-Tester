#!/usr/bin/env python3
"""Ubuntu Mirror Speed Tester"""


import csv
import shlex
import subprocess
import sys
import time
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


# Function to get download speed
def get_download_speed(url):
    """
    Function to return download speed for a given URL.
    """
    # Try to run the HTTP request and download the file
    try:
        data = requests.get(url, stream=True, timeout=10)
        if response.status_code != 200:
            print(
                f"Received HTTP status code {response.status_code} while fetching the file")
            return 0
        total_size = int(data.headers.get("Content-Length", 0))
        downloaded_size = 0
        start_time = time.time()
        with open("/dev/null", "wb") as download_file:
            for data in data.iter_content(1024):
                downloaded_size += len(data)
                download_file.write(data)
        elapsed_time = time.time() - start_time
        return total_size // elapsed_time
    except requests.exceptions.RequestException:
        print("An error occurred while getting the file from:", full_url)
        return 0


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


# Function to write CSV
def write_to_csv(results, filename, header):
    """
    Function to write CSV
    """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for each_result in results:
            writer.writerow(each_result)


# Try to retrieve the mirrors list from the specified URL
MIRROR_URL = "http://mirrors.ubuntu.com/mirrors.txt"
try:
    print("Getting Mirrors List from:", MIRROR_URL)
    response = requests.get(MIRROR_URL, timeout=10)
    if response.status_code != 200:
        print("Getting mirrors list failed")
        sys.exit(1)
    mirrors = response.text.splitlines()
    print("Received", len(mirrors), "Ubuntu Mirror Server(s)")
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
    ping_command = shlex.split(f"ping -c 3 {hostname}")
    download_speed = get_download_speed(full_url)
    if download_speed == 0:
        continue
    icmp_check = False
    try:
        # Try to ping the mirror and capture the output
        ping_output = subprocess.run(
            ping_command, capture_output=True, check=True).stdout.decode("utf-8")
        icmp_check = True
    except subprocess.CalledProcessError:
        print(f"An error occurred while pinging mirror {hostname}")
    if icmp_check is True:
        parsed_ping_output = jc.parse("ping", ping_output)
        average_ping = f'{parsed_ping_output["round_trip_ms_avg"]} ms'
        packet_loss = f'{parsed_ping_output["packet_loss_percent"]}%'
    else:
        average_ping = "na"
        packet_loss = "na"
    result = [hostname, full_url, average_ping, packet_loss,
              download_speed, sizeof_fmt(float(download_speed))]
    mirror_results.append(result)


if mirror_results:
    write_to_csv(mirror_results, "result.csv", HEADER)
    print("")
    print(tabulate(mirror_results, HEADER))
else:
    print("Script finished with errors...")

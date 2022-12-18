#!/usr/bin/env python3


import jc
import subprocess
import shlex
import requests
from urllib.parse import urlparse
from time import sleep


def sizeof_fmt(num, suffix="B/s"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


response = requests.get("http://mirrors.ubuntu.com/mirrors.txt", timeout=10)
if response.status_code != 200:
    print("Getting mirrors list failed")
    exit(1)
mirrors = response.text.splitlines()
print(", ".join(["Hostname", "Full URL", "Average Latency (ms)", "Packet Loss (%)", "Download Speed (Bytes)", "Download Speed"]))
print("")
for mirror in mirrors:
    hostname = urlparse(mirror).hostname
    full_url = mirror + "dists/jammy/Contents-amd64.gz"
    command = "curl -qfsLS -w '%{speed_download}' -o /dev/null --url" + " " + full_url
    curl_command = shlex.split(command)
    try:
        curl_speed_in_bytes = subprocess.run(curl_command, capture_output=True).stdout.decode("utf-8")
        if curl_speed_in_bytes == 0:
            continue
        ping_output = subprocess.check_output(["ping", "-c", "10", "-i", "0.25", hostname], text=True)
    except subprocess.CalledProcessError:
        continue
    parsed_ping_output = jc.parse("ping", ping_output)
    average_ping = parsed_ping_output["round_trip_ms_avg"]
    packet_loss = parsed_ping_output["packet_loss_percent"]
    result = ", ".join([hostname, full_url, f"{average_ping} ms", f"{packet_loss}%", curl_speed_in_bytes, sizeof_fmt(float(curl_speed_in_bytes))])
    print(result)

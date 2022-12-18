# Ubuntu Mirror Speed Tester

This script retrieves a list of mirrors from a specified URL, pings each mirror to measure its average latency and packet loss, and then uses `curl` to download a file from each mirror and measure its download speed. The results are printed to the console in a table format.

## Requirements

* Python 3
* The `jc` library (install using `pip install jc`)
* The `requests` library (install using `pip install requests`)

## Usage
To run the script, use the following command:

```
python3 main.py
```

By default, the script retrieves the mirrors list from `http://mirrors.ubuntu.com/mirrors.txt` and downloads the file `dists/jammy/Contents-amd64.gz` from each mirror. You can customize these settings by modifying the script.

## Output
The script prints the following information for each mirror:

* Hostname: the hostname of the mirror
* Full URL: the full URL of the file that was downloaded
* Average Latency (ms): the average round-trip time for pings to the mirror, in milliseconds
* Packet Loss (%): the percentage of pings that were lost
* Download Speed (Bytes): the download speed of the file, in bytes per second
* Download Speed: the download speed of the file, formatted in a human-readable format (e.g. "1.2 MiB/s")

## Examples

Here is an example of the output produced by the script:

```
Hostname, Full URL, Average Latency (ms), Packet Loss (%), Download Speed (Bytes), Download Speed

in.mirror.coganng.com, https://in.mirror.coganng.com/ubuntu/dists/jammy/Contents-amd64.gz, 31.479 ms, 0.0%, 10215357, 9.7 MiB/s
repos.del.extreme-ix.org, http://repos.del.extreme-ix.org/ubuntu/dists/jammy/Contents-amd64.gz, 10.021 ms, 0.0%, 14168699, 13.5 MiB/s
ubuntu.hbcse.tifr.res.in, http://ubuntu.hbcse.tifr.res.in/ubuntu/dists/jammy/Contents-amd64.gz, 33.364 ms, 0.0%, 12950277, 12.4 MiB/s
in.mirror.coganng.com, https://in.mirror.coganng.com/ubuntu-ports/dists/jammy/Contents-amd64.gz, 31.425 ms, 0.0%, 0, 0.0 B/s
mirrors.piconets.webwerks.in, http://mirrors.piconets.webwerks.in/ubuntu-mirror/ubuntu/dists/jammy/Contents-amd64.gz, 34.411 ms, 0.0%, 17579970, 16.8 MiB/s
repo.extreme-ix.org, https://repo.extreme-ix.org/ubuntu/dists/jammy/Contents-amd64.gz, 9.199 ms, 0.0%, 13905416, 13.3 MiB/s
ftp.iitm.ac.in, http://ftp.iitm.ac.in/ubuntu/dists/jammy/Contents-amd64.gz, 44.134 ms, 0.0%, 12862257, 12.3 MiB/s
```


## Contributions
Feel free to fork the repository and submit pull requests with any improvements or modifications to the script.

## License
This project is licensed under the MIT License - see the **[LICENSE](LICENSE)** file for details.

#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages (ps: with ps; [ requests ])"

import re
import json
import os
import urllib.parse
import sys

import requests

BASE_URL = "https://dl.sipeed.com/fileList/"

def main():
    download_dir("LICHEE/D1/Lichee_RV")
    download_dir("LICHEE/D1/Lichee_RV-Dock")
    download_dir("LICHEE/D1/Lichee_RV_86_panel")


def download_dir(dir):
    url = BASE_URL + dir
    print(f"Getting {url}")

    r = requests.get(url)

    if r.status_code != 200:
        print(f"Failed to get page '{url}', code: {r.status_code}")
        return

    directory_info = r.json()

    os.makedirs(directory_info['this_path'], exist_ok = True)

    for entry in directory_info['data']:
        if entry['file_type'] == 0:
            # Directory.
            download_dir(entry['file_url'])
        elif entry['file_type'] == 1:
            # File.
            download_to_file(BASE_URL + entry['file_url'], entry['file_url'])


def download_to_file(url, destination):
    print(f"Downloading '{url}' to '{destination}'")

    r = requests.get(url)

    if r.status_code != 200:
        print(f"Download failed, code: {r.status_code}")
        return

    with open(destination, "wb") as f:
        f.write(r.content)


if __name__ == "__main__":
    main()

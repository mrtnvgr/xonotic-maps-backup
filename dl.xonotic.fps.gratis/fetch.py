#!/usr/bin/env python3

from urllib.request import urlretrieve
from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests, os

URL = "http://dl.xonotic.fps.gratis"

BROKEN_MAPS = ["radio"]

MAPS_PATH = "maps"

@dataclass
class Map:
    file: str
    size: int

def download(url, path):
    try:
        urlretrieve(url, path)
    except:
        print(f"Downloading failed! Removing incomplete file \"{path}\"...")
        os.remove(path)

def get_soup(url):
    print("Downloading index...")
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

root = get_soup(URL)

maps = []
for entry in root.find_all("tr", "file"):
    file = entry.find("a", "name").text
    size = entry.find_all("td")[2]["sorttable_customkey"]

    if not size.isdigit():
        if file not in BROKEN_MAPS:
            print(f"WARN: \"{file}\" map is broken")
        continue

    maps.append(Map(file, int(size)))

def keep_only_missing_maps(map_: Map):
    path = os.path.join(MAPS_PATH, map_.file)
    path_exists = os.path.exists(path)
    size = os.path.getsize(path) if path_exists else -1
    return (not path_exists) or size != map_.size

maps = list(filter(keep_only_missing_maps, maps))

maps_count = len(maps)
print(f"Found {maps_count} new maps.")

for i, map_ in enumerate(maps):
    map_url = f"{URL}/{map_.file}"
    map_path = os.path.join(MAPS_PATH, map_.file)

    download(map_url, map_path)

    print(f"[{i+1}/{maps_count}] {map_.file}")

# ==================================================================

# WARN: misc downloader does not check file sizes!
#       please re-download ALL of the filess if something went wrong :)
def misc_downloader(name):
    url = f"{URL}/{name}"

    root = get_soup(url)

    files = [file["href"] for file in root.find_all("a")]
    files = [file for file in files if "." in file]

    files_dir = f"{name}s"

    def keep_only_missing(x: str):
        path = os.path.join(files_dir, x)
        path_exists = os.path.exists(path)
        return not path_exists

    files = list(filter(keep_only_missing, files))

    file_count = len(files)

    print(f"Found {file_count} new {name}s.")

    for i, file in enumerate(files):
        file_url = f"{url}/{file}"
        file_path = os.path.join(files_dir, file)

        download(file_url, file_path)

        print(f"[{i+1}/{file_count}] {file}")

# === Download other directories
misc_downloader("ent")
misc_downloader("shh")

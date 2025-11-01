#!/usr/bin/env python3

from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests, glob, sys, os

LATEST_PATH = "latest_versions"
ALL_FILES_PATH = "all_files"

def get_map_name(map_file: str) -> str:
    return map_file.split("-full")[0]

EXPECTED_FILES = {"fetch.py", LATEST_PATH, ALL_FILES_PATH}
if set(os.listdir(".")) != EXPECTED_FILES:
    print("Error: unexpected files in working dir")
    sys.exit(1)

for f in glob.glob(os.path.join(LATEST_PATH, "*.pk3")):
    os.remove(f)

print("Downloading index...")

url = "http://beta.xonotic.org/autobuild-bsp"
response = requests.get(url)

root = BeautifulSoup(response.text, "html.parser")

entries = root.find_all("tr", ["row1", "row0"])

map_files = [entry.find("td", "fullpk3").a["href"] for entry in entries]
map_files_count = len(map_files)

maps_in_latest = set()
latest_versions = []

for map_file in map_files:
    map_name = get_map_name(map_file)

    if map_name not in maps_in_latest:
        maps_in_latest.add(map_name)
        latest_versions.append(map_file)

# If symlinking fails after ALL of the maps have been downloaded,
# that would be sad :/
print(f"Symlinking {len(latest_versions)} maps...")

for latest_version in latest_versions:
    map_name = latest_version.split("-full")[0]

    map_path  = os.path.join("..", ALL_FILES_PATH, map_name, latest_version)
    link_path = os.path.join(      LATEST_PATH,              latest_version)

    os.symlink(map_path, link_path)

for i, map_file in enumerate(map_files):
    map_url = f"{url}/{map_file}"

    map_name = get_map_name(map_file)
    map_path = os.path.join(ALL_FILES_PATH, map_name, map_file)

    if not os.path.exists(map_path):
        urlretrieve(map_url, map_path)

    print(f"[{i+1}/{map_files_count}] {map_file}")

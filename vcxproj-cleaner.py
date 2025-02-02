import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

parser = argparse.ArgumentParser(
        prog = "Visual Studio Solution Cleaner",
        description = "Clears deleted file references from solution.",
        )

parser.add_argument('path')
args = parser.parse_args()

include_pattern = re.compile(r'Include\s*=\s*"([^"]*)"')

root_path = Path(args.path)

vcxprojs = list(root_path.glob("*.vcxproj"))
vcxproj_filters = list(root_path.glob("*.vcxproj.filters"))

if not vcxprojs or not vcxproj_filters:
    print("ERROR: No vcxproj files found in specified path.")
    sys.exit()

print(f"INFO:: Found vcxproj files for solution at \"{root_path}\".")

ns = {"msbuild": "http://schemas.microsoft.com/developer/msbuild/2003"} 
vcxproj_files = [vcxprojs[0], vcxproj_filters[0]]
removed_count = 0
for vcxproj in vcxproj_files:
    tree = ET.parse(vcxproj)
    tree_root = tree.getroot()
    item_groups = tree_root.findall(".//msbuild:ItemGroup", namespaces = ns)
    item_groups = [ig for ig in item_groups if ig.get("Label") != "ProjectConfigurations"]

    sub_removed_count = 0
    for group in item_groups:
        for x in list(group.findall("*[@Include]")):
            include_path = x.get("Include")
            file_path = root_path / Path(include_path)
            if not file_path.is_file():
                print(f"INFO::Detected bad reference for {file_path}. Removing from vcxproj.")
                group.remove(x)
                sub_removed_count = sub_removed_count + 1
                removed_count = removed_count + 1

    if sub_removed_count > 0:
        tree.write(vcxproj, encoding="utf-8", xml_declaration=True)

print(f"DONE:: Removed {removed_count} bad references from solution.")

        
#!/usr/bin/env python3
import json
import os.path
import pathlib

with open("boundaries.json", "rb") as f:
    info = json.load(f)
print("boundaries - Version: " + info["version"])

os.system("chmod +x main.py")

print("Checking Folder Structure...")
os.chdir("../..")

if not os.path.exists("var"):
    print("Warning: var dir does not exist. Creating it...")
    pathlib.Path("var").mkdir()
    pathlib.Path("var/boundaries").mkdir()

if not os.path.exists("exec"):
    print("Warning: exec dir does not exist. Creating it...")
    pathlib.Path("exec").mkdir()
    pathlib.Path("exec/bin").mkdir()
    pathlib.Path("exec/desktop").symlink_to(os.path.realpath(os.path.expanduser("~/.local/share/applications")))

if not os.path.exists("exec/bin"):
    print("Warning: exec/bin dir does not exist. Creating it...")
    pathlib.Path("exec/bin").mkdir()

if not os.path.exists("exec/desktop"):
    print("Warning: exec/desktop dir does not exist. Making a Symlink...")
    pathlib.Path("exec/desktop").symlink_to(os.path.realpath(os.path.expanduser("~/.local/share/applications")))

if not os.path.exists("bin"):
    print("Warning: bin dir does not exist. Making a Symlink...")
    pathlib.Path("bin").symlink_to("apps/boundaries")

print("Folder Structure checking done")

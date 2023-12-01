#!/bin/python3
import os
import sys
import shutil
import json

BND_DIR = os.path.realpath(os.path.expanduser("~/boundaries/bin"))
APP_DIR = os.path.realpath(os.path.join(os.path.join(BND_DIR, ".."), "apps"))
EXEC_DIR = os.path.realpath(os.path.join(os.path.join(BND_DIR, ".."), "exec"))


def remove(filename):
    shutil.rmtree(os.path.join(APP_DIR, filename))


def run(filename, args):
    packagefolder = os.path.join(APP_DIR, filename)
    os.chdir(packagefolder)
    os.system("pwd")
    infofile = os.path.join(packagefolder, "boundaries.json")
    if os.path.exists(infofile):
        with open(infofile, "rb") as f:
            info = json.loads(f.read())
    else:
        print(f"Error: Cannot find {infofile}")
    run_command = info["commands"]["run"]
    for a in args:
        run_command = run_command + " " + a
    os.system(run_command)


def install(filepath):
    filepath = os.path.realpath(os.path.join(os.getcwd(), filepath))
    if not os.path.isdir(filepath):
        pkg = True
        packagefolder = os.path.join("/tmp", "boundaries")
        print(f"Unpacking {filepath}...")
        shutil.unpack_archive(filepath, packagefolder)
        packagefolder = os.path.join(packagefolder, os.listdir(packagefolder)[0])
    else:
        pkg = False
        packagefolder = filepath
    infofile = os.path.join(packagefolder, "boundaries.json")
    if os.path.exists(infofile):
        with open(infofile, "rb") as f:
            info = json.loads(f.read())
    else:
        print(f"Error: Cannot find {infofile}")
    pkg_name = info["name"]
    if pkg:
        shutil.move(packagefolder, os.path.join(APP_DIR, pkg_name))
    else:
        shutil.copytree(packagefolder, os.path.join(APP_DIR, pkg_name))
    packagefolder = os.path.join(APP_DIR, pkg_name)
    os.chdir(packagefolder)
    os.system("pwd")
    infofile = os.path.join(packagefolder, "boundaries.json")
    if os.path.exists(infofile):
        with open(infofile, "rb") as f:
            info = json.loads(f.read())
    else:
        print(f"Error: Cannot find {infofile}")
    try:
        custom_install_command = info["commands"]["install"]
        custom_install_command_available = True
    except:
        custom_install_command_available = False
    if custom_install_command_available:
        print(f"Running Comand \"{custom_install_command}\"...")
        custom_install_command_success = os.system(custom_install_command)
    else:
        print("No Command to Run.")
        custom_install_command_success = 0
    if custom_install_command_success == 0:
        print(f"{pkg_name} installed succesfully.")
        with open(os.path.realpath(f"{EXEC_DIR}/desktop/{pkg_name}.desktop"), "w") as f:
            d = f"[Desktop Entry]\nName={pkg_name}\nExec={__file__} -r \"{pkg_name}\"\nIcon={os.path.join(packagefolder, info['icon'])}\nTerminal=false\nType=Application\nCategories=boundaries;\nStartupNotify=true;\nPath={packagefolder}"
            f.write(d)
    else:
        print(f"{pkg_name} was not installed succesfully.")


if __name__ == '__main__':
    try:
        action = sys.argv[1]
    except:
        print("Error: No Argument given")
        action = ""
    if action == "--install" or action == "-i":
        install(sys.argv[2])
    elif action == "--run" or action == "-r":
        run(sys.argv[2], sys.argv[3:])
    elif action == "--remove":
        remove(sys.argv[2])
    else:
        print(f"Error: Invalid Argument \"{action}\"")

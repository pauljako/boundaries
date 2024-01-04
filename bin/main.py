#!/bin/python3
import os
import sys
import shutil
import json

BND_DIR = os.path.realpath(os.path.expanduser("~/boundaries/bin"))
APP_DIR = os.path.realpath(os.path.join(os.path.join(BND_DIR, ".."), "apps"))
EXEC_DIR = os.path.realpath(os.path.join(os.path.join(BND_DIR, ".."), "exec"))


def getpkginfo(packagename: str) -> dict | None:
    pkgpath = os.path.join(APP_DIR, packagename)
    pkginfopath = os.path.join(pkgpath, "boundaries.json")
    if os.path.isdir(pkgpath) and os.path.exists(pkginfopath):
        with open(pkginfopath, "rb") as f:
            info = json.loads(f.read())
        return info
    else:
        return None


def listpkgs():
    print("Name:")
    for p in os.listdir(APP_DIR):
        info = getpkginfo(p)
        if info is not None and "name" in info:
            if "de_name" in info:
                de_name = info["de_name"]
            else:
                de_name = info["name"]
            if "version" in info:
                version = f" {str(info['version'])}"
            else:
                version = ""
            print(f"{info['name']} ({de_name}{version})")


def remove(filename):
    info = getpkginfo(filename)
    print(f"Removing Files of {info['name']}")
    shutil.rmtree(os.path.join(APP_DIR, filename))
    if os.path.exists(os.path.realpath(f"{EXEC_DIR}/desktop/{filename}.desktop")):
        print("Removing Desktop Entry")
        os.remove(os.path.realpath(f"{EXEC_DIR}/desktop/{filename}.desktop"))
    if "bin" in info:
        print("Removing Command")
        os.remove(os.path.realpath(f"{EXEC_DIR}/bin/{info['bin']}"))


def run(filename, args):
    info = getpkginfo(filename)
    package_folder = os.path.join(APP_DIR, filename)
    os.chdir(package_folder)
    if info is None:
        print(f"Error: Cannot find the boundaries.json file")
    run_command = info["command"]["run"]
    for a in args:
        run_command = run_command + " " + a
    os.system(run_command)


def install(filepath):
    filepath = os.path.realpath(os.path.join(os.getcwd(), filepath))
    if not os.path.isdir(filepath):
        pkg = True
        package_folder = os.path.join("/tmp", "boundaries")
        print(f"Unpacking {filepath}...")
        shutil.unpack_archive(filepath, package_folder)
        for f in os.listdir(package_folder):
            if f == "boundaries.json":
                break
            elif os.path.isdir(os.path.join(package_folder, f)):
                package_folder = os.path.join(package_folder, f)
    else:
        pkg = False
        package_folder = filepath
    infofile = os.path.join(package_folder, "boundaries.json")
    if os.path.exists(infofile):
        with open(infofile, "rb") as f:
            info = json.loads(f.read())
    else:
        print(f"Error: Cannot find {infofile}")
        return False
    if "name" in info and "command" in info and "run" in info["command"]:
        pkg_name = info["name"]
    else:
        print("The boundaries.json file did not provide enough necessary information")
        return False
    if os.path.exists(os.path.join(APP_DIR, pkg_name)) and os.path.isdir(os.path.join(APP_DIR, pkg_name)):
        if input("The Package is already installed. Do you want to delete the existing one? (Y/n)") == "n":
            return False
        else:
            remove(pkg_name)
    if pkg:
        shutil.move(package_folder, os.path.join(APP_DIR, pkg_name))
    else:
        shutil.copytree(package_folder, os.path.join(APP_DIR, pkg_name))
    package_folder = os.path.join(APP_DIR, pkg_name)
    os.chdir(package_folder)
    os.system("pwd")
    infofile = os.path.join(package_folder, "boundaries.json")
    if os.path.exists(infofile):
        with open(infofile, "rb") as f:
            info = json.loads(f.read())
    else:
        print(f"Error: Cannot find {infofile}")
    custom_install_command_available = "install" in info["command"]
    if custom_install_command_available:
        custom_install_command = info["command"]["install"]
        print(f"Running Comand \"{custom_install_command}\"...")
        custom_install_command_success = os.system(custom_install_command)
    else:
        print("No Command to Run.")
        custom_install_command_success = 0
    if custom_install_command_success == 0:
        if "de_name" in info:
            de_name = info["de_name"]
        else:
            de_name = pkg_name
        print(f"{pkg_name} installed successfully.")
        if "icon" in info:
            print("Creating Desktop Entry")
            with open(os.path.realpath(f"{EXEC_DIR}/desktop/{pkg_name}.desktop"), "w") as f:
                d = f"[Desktop Entry]\nName={de_name}\nExec={os.path.join(BND_DIR, 'main.py')} -r \"{pkg_name}\"\nIcon={os.path.join(package_folder, info['icon'])}\nTerminal=false\nType=Application\nCategories=boundaries;\nStartupNotify=true;\nPath={package_folder}"
                f.write(d)
        else:
            print("No Icon. Not creating a .desktop File.")
        if "bin" in info:
            print("Creating Command")
            binpath = os.path.realpath(f"{EXEC_DIR}/bin/{info['bin']}")
            with open(binpath, "w") as f:
                d = f'#!/bin/bash\ni="";\nfor arg in "$@"\ndo\ni="$i $arg";\ndone\n{__file__} -r \"{pkg_name}\" $i'
                f.write(d)
            print("Making Command Executable")
            os.system(f'chmod +x {binpath}')
        return True
    else:
        print(f"Install Command failed")
        return False


if __name__ == '__main__':
    try:
        action = sys.argv[1]
    except:
        print("Error: No Argument given")
        action = ""
    if action == "--install" or action == "-i":
        if install(sys.argv[2]):
            print(f"{sys.argv[2]} was installed successfully")
        else:
            print(f"{sys.argv[2]} was not installed successfully")
    elif action == "--run" or action == "-r":
        run(sys.argv[2], sys.argv[3:])
    elif action == "--remove":
        remove(sys.argv[2])
    elif action == "--list":
        listpkgs()
    else:
        print(f"Error: Invalid Argument \"{action}\"")

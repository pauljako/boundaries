#!/bin/python3
import os
import pathlib
import sys
import shutil
import json


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


QUOTE_SYMBOL_DOING = f"{Colors.OKCYAN}::{Colors.ENDC}"
QUOTE_SYMBOL_WARNING = f"{Colors.WARNING}::{Colors.ENDC}"
QUOTE_SYMBOL_INFO = f"{Colors.OKGREEN}::{Colors.ENDC}"
QUOTE_SYMBOL_ERROR = f"{Colors.FAIL}::{Colors.ENDC}"
BND_DIR = os.path.realpath(os.path.join(os.path.realpath(os.path.expanduser("~/boundaries/bin")), ".."))
APP_DIR = os.path.realpath(os.path.join(os.path.join(BND_DIR, ".."), "apps"))
EXEC_DIR = os.path.realpath(os.path.join(os.path.join(BND_DIR, ".."), "exec"))
VAR_DIR = os.path.realpath(os.path.join(os.path.join(BND_DIR, ".."), "var"))
BND_DIR = os.path.realpath(os.path.join(APP_DIR, "boundaries"))


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
    print("Installed Packages:")
    dir_content = sorted(os.listdir(APP_DIR))
    for p in dir_content:
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


def remove(filename, keep_data=False):
    info = getpkginfo(filename)
    print(f"{QUOTE_SYMBOL_DOING}Removing Files of {info['name']}{QUOTE_SYMBOL_DOING}")
    shutil.rmtree(os.path.join(APP_DIR, filename))
    if not keep_data:
        print(f"{QUOTE_SYMBOL_DOING}Removing Data of {info['name']}{QUOTE_SYMBOL_DOING}")
        shutil.rmtree(os.path.join(VAR_DIR, filename))
    if os.path.exists(os.path.realpath(f"{EXEC_DIR}/desktop/{filename}.desktop")):
        print(f"{QUOTE_SYMBOL_DOING}Removing Desktop Entry{QUOTE_SYMBOL_DOING}")
        os.remove(os.path.realpath(f"{EXEC_DIR}/desktop/{filename}.desktop"))
    if "bin" in info:
        print(f"{QUOTE_SYMBOL_DOING}Removing Command{QUOTE_SYMBOL_DOING}")
        os.remove(os.path.realpath(f"{EXEC_DIR}/bin/{info['bin']}"))


def run(filename, args):
    info = getpkginfo(filename)
    package_folder = os.path.join(APP_DIR, filename)
    var_folder = os.path.join(VAR_DIR, filename)
    org_dir = os.getcwd()
    # os.chdir(package_folder)
    if info is None:
        print(f"{QUOTE_SYMBOL_ERROR}Cannot find the boundaries.json file{QUOTE_SYMBOL_ERROR}")
    run_command = f"APP_DIR={package_folder} VAR_DIR={var_folder} "
    run_command = run_command + os.path.realpath(os.path.join(package_folder, info["command"]["run"]))
    for a in args:
        run_command = run_command + " " + a
    print(f"{QUOTE_SYMBOL_DOING}Running {filename}{QUOTE_SYMBOL_DOING}")
    os.system(run_command)


def install(filepath):
    filepath = os.path.realpath(os.path.join(os.getcwd(), filepath))
    if not os.path.isdir(filepath):
        pkg = True
        package_folder = os.path.join("/tmp", "boundaries")
        print(f"{QUOTE_SYMBOL_DOING}Unpacking {filepath}{QUOTE_SYMBOL_DOING}")
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
        print(f"{QUOTE_SYMBOL_ERROR}Cannot find {infofile}{QUOTE_SYMBOL_ERROR}")
        return False
    if "name" in info and "command" in info and "run" in info["command"]:
        pkg_name = info["name"]
    else:
        print(f"{QUOTE_SYMBOL_ERROR}The boundaries.json file did not provide enough necessary information{QUOTE_SYMBOL_ERROR}")
        return False
    if os.path.exists(os.path.join(APP_DIR, pkg_name)) and os.path.isdir(os.path.join(APP_DIR, pkg_name)):
        if input(f"{QUOTE_SYMBOL_WARNING}The Package is already installed. Do you want to delete the existing one? (Y/n) ") == "n":
            return False
        else:
            remove(pkg_name, True)
    if pkg:
        shutil.move(package_folder, os.path.join(APP_DIR, pkg_name))
    else:
        shutil.copytree(package_folder, os.path.join(APP_DIR, pkg_name))
    package_folder = os.path.join(APP_DIR, pkg_name)
    os.chdir(package_folder)
    # os.system("pwd")
    infofile = os.path.join(package_folder, "boundaries.json")
    if os.path.exists(infofile):
        with open(infofile, "rb") as f:
            info = json.loads(f.read())
    else:
        print(f"{QUOTE_SYMBOL_ERROR}Cannot find {infofile}{QUOTE_SYMBOL_ERROR}")
        return False
    if not os.path.exists(os.path.join(VAR_DIR, pkg_name)):
        print(f"{QUOTE_SYMBOL_DOING}Creating Data Directory{QUOTE_SYMBOL_DOING}")
        pathlib.Path(os.path.join(VAR_DIR, pkg_name)).mkdir()
    custom_install_command_available = "install" in info["command"]
    if custom_install_command_available:
        custom_install_command = info["command"]["install"]
        print(f"{QUOTE_SYMBOL_DOING}Running Command \"{custom_install_command}\"{QUOTE_SYMBOL_DOING}")
        custom_install_command_success = os.system(custom_install_command)
    else:
        print(f"{QUOTE_SYMBOL_INFO}No Command to Run.{QUOTE_SYMBOL_INFO}")
        custom_install_command_success = 0
    if custom_install_command_success == 0:
        if "de_name" in info:
            de_name = info["de_name"]
        else:
            de_name = pkg_name
        if "icon" in info:
            print(f"{QUOTE_SYMBOL_DOING}Creating Desktop Entry{QUOTE_SYMBOL_DOING}")
            desktop_path = os.path.realpath(f"{EXEC_DIR}/desktop/{pkg_name}.desktop")
            with open(desktop_path, "w") as f:
                d = f"[Desktop Entry]\nName={de_name}\nExec={os.path.join(BND_DIR, 'main.py')} -r \"{pkg_name}\"\nIcon={os.path.join(package_folder, info['icon'])}\nTerminal=false\nType=Application\nCategories=boundaries;\nStartupNotify=true;\nPath={package_folder}"
                f.write(d)
            print(f"{QUOTE_SYMBOL_DOING}Making Desktop Entry Executable{QUOTE_SYMBOL_DOING}")
            os.system(f'chmod +x {desktop_path}')
        else:
            print(f"{QUOTE_SYMBOL_INFO}No Icon. Not creating a .desktop File.{QUOTE_SYMBOL_INFO}")
        if "bin" in info:
            print(f"{QUOTE_SYMBOL_DOING}Creating Command {info['bin']}{QUOTE_SYMBOL_DOING}")
            binpath = os.path.realpath(f"{EXEC_DIR}/bin/{info['bin']}")
            with open(binpath, "w") as f:
                d = f'#!/bin/bash\ni="";\nfor arg in "$@"\ndo\ni="$i $arg";\ndone\n{os.path.join(BND_DIR, "main.py")} -r \"{pkg_name}\" $i'
                f.write(d)
            print(f"{QUOTE_SYMBOL_DOING}Making Command Executable{QUOTE_SYMBOL_DOING}")
            os.system(f'chmod +x {binpath}')
        print(f"{QUOTE_SYMBOL_INFO}{pkg_name} installed successfully.{QUOTE_SYMBOL_INFO}")
        return True
    else:
        print(f"{QUOTE_SYMBOL_ERROR}Install Command failed{QUOTE_SYMBOL_ERROR}")
        return False


if __name__ == '__main__':
    if len(sys.argv) > 1:
        action = sys.argv[1]
    else:
        print(f"{QUOTE_SYMBOL_ERROR}No Argument given{QUOTE_SYMBOL_ERROR}")
        exit()
    if action == "--install" or action == "-i":
        if len(sys.argv) != 3:
            print(f"{QUOTE_SYMBOL_ERROR}The Command Requires Exactly 1 Argument{QUOTE_SYMBOL_ERROR}")
            exit()
        if install(sys.argv[2]):
            print(f"{QUOTE_SYMBOL_INFO}{sys.argv[2]} was installed successfully{QUOTE_SYMBOL_INFO}")
        else:
            print(f"{QUOTE_SYMBOL_ERROR}{sys.argv[2]} was not installed successfully{QUOTE_SYMBOL_ERROR}")
    elif action == "--run" or action == "-r":
        if len(sys.argv) < 3:
            print(f"{QUOTE_SYMBOL_ERROR}The Command Requires at least 1 Argument{QUOTE_SYMBOL_ERROR}")
            exit()
        run(sys.argv[2], sys.argv[3:])
    elif action == "--remove":
        if len(sys.argv) != 3:
            print(f"{QUOTE_SYMBOL_ERROR}The Command Requires Exactly 1 Argument{QUOTE_SYMBOL_ERROR}")
            exit()
        remove(sys.argv[2])
    elif action == "--list":
        if len(sys.argv) != 2:
            print(f"{QUOTE_SYMBOL_ERROR}The Command Requires Exactly 0 Arguments{QUOTE_SYMBOL_ERROR}")
            exit()
        listpkgs()
    else:
        print(f"{QUOTE_SYMBOL_ERROR}Invalid Argument \"{action}\"{QUOTE_SYMBOL_ERROR}")

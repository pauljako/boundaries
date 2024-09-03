#!/usr/bin/env python3
import os
import pathlib
import sys
import shutil
import json
import argparse
import importlib


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


QUOTE_SYMBOL_DOING = f" {Colors.BOLD}{Colors.OKCYAN}::{Colors.ENDC} "
QUOTE_SYMBOL_WARNING = f" {Colors.BOLD}{Colors.WARNING}::{Colors.ENDC} "
QUOTE_SYMBOL_INFO = f" {Colors.BOLD}{Colors.OKGREEN}::{Colors.ENDC} "
QUOTE_SYMBOL_ERROR = f" {Colors.BOLD}{Colors.FAIL}::{Colors.ENDC} "
QUOTE_SYMBOL_OUTPUT = f" {Colors.BOLD}{Colors.OKBLUE}::{Colors.ENDC} "
SIMPLE = False

if os.path.exists(os.path.expanduser("~/.bndpath")):
    with open(os.path.expanduser("~/.bndpath"), "r") as file:
        path = file.readline().strip().replace("\n", "")
        if os.path.exists(os.path.expanduser(path)):
            BND_DIR = os.path.realpath(os.path.join(os.path.expanduser(path), "apps"))
        else:
            print(f"{QUOTE_SYMBOL_ERROR}The path {path} does not exist. Please fix your ~/.bndpath file. Using default{QUOTE_SYMBOL_ERROR}")
            BND_DIR = os.path.realpath(os.path.join(os.path.realpath(os.path.expanduser("~/boundaries/apps")), "."))
else:
    BND_DIR = os.path.realpath(os.path.join(os.path.realpath(os.path.expanduser("~/boundaries/apps")), "."))

APP_DIR = os.path.realpath(os.path.join(os.path.join(BND_DIR, ".."), "apps"))
EXEC_DIR = os.path.realpath(os.path.join(os.path.join(BND_DIR, ".."), "exec"))
VAR_DIR = os.path.realpath(os.path.join(os.path.join(BND_DIR, ".."), "var"))
PLUGIN_DIR = os.path.realpath(os.path.join(os.path.join(BND_DIR, ".."), "plugins"))
BND_DIR = os.path.realpath(os.path.join(APP_DIR, "boundaries"))
with open(os.path.realpath(os.path.join(BND_DIR, "boundaries.json")), "rb") as f:
    VERSION = json.load(f)["version"]


def load_plugins() -> dict:
    plugins = {
        "extends": {
            "run": {},
            "install": {},
            "remove": {},
        },
        "custom": {}
    }
    if not os.path.exists(PLUGIN_DIR):
        return {}
    for p in sorted(os.listdir(PLUGIN_DIR)):
        path = os.path.realpath(os.path.join(PLUGIN_DIR, p))
        sys.path.insert(1, path)
        if not (os.path.exists(path) or os.path.isdir(path) or os.path.exists(os.path.join(path, "plugin.json"))):
            break
        with open(os.path.join(path, "plugin.json"), "rb") as f:
            pluginspec = json.load(f)
        if ("name" not in pluginspec):
            break
        if "extends" in pluginspec:
            for k, v in pluginspec["extends"].items():
                if k == "run":
                    plugins["extends"]["run"][pluginspec["name"]] = importlib.import_module(v, path)
                if k == "install":
                    plugins["extends"]["install"][pluginspec["name"]] = importlib.import_module(v, path)
                if k == "remove":
                    plugins["extends"]["remove"][pluginspec["name"]] = importlib.import_module(v, path)
        if "custom" in pluginspec:
            for k, v in pluginspec["custom"].items():
                if pluginspec["name"] not in plugins["custom"]:
                    plugins["custom"][pluginspec["name"]] = {}
                plugins["custom"][pluginspec["name"]][k] = importlib.import_module(v, path)
    return plugins
        
PLUGINS = load_plugins()

def getpkginfo(packagename: str) -> dict | None:
    pkgpath = os.path.join(APP_DIR, packagename)
    pkginfopath = os.path.join(pkgpath, "boundaries.json")
    if os.path.isdir(pkgpath) and os.path.exists(pkginfopath):
        with open(pkginfopath, "rb") as f:
            info = json.loads(f.read())
        return info
    else:
        return None


def get_packages() -> list:
    pkgs = []
    dir_content = sorted(os.listdir(APP_DIR))
    for p in dir_content:
        path = os.path.realpath(os.path.join(APP_DIR, p))
        if os.path.exists(path) and os.path.isdir(path) and (getpkginfo(p) is not None):
            pkgs.append(p)
    return pkgs


def listpkgs():
    if not SIMPLE:
        print(f"{QUOTE_SYMBOL_OUTPUT}Installed Packages:")
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
                print(f"{QUOTE_SYMBOL_OUTPUT}{info['name']} ({de_name}{version})")
    else:
        dir_content = sorted(os.listdir(APP_DIR))
        for p in dir_content:
            info = getpkginfo(p)
            if info is not None and "name" in info:
                print(f"{QUOTE_SYMBOL_OUTPUT}{info['name']}")


def remove(filename, keep_data=False):
    info = getpkginfo(filename)
    for k, v in PLUGINS["extends"]["remove"].items():
        if not SIMPLE: print(f"{QUOTE_SYMBOL_DOING}Running Plugin {k}{QUOTE_SYMBOL_DOING}")
        v.execute(filename, info, keep_data)
    print(f"{QUOTE_SYMBOL_DOING}Removing Files of {info['name']}{QUOTE_SYMBOL_DOING}")
    shutil.rmtree(os.path.join(APP_DIR, filename))
    if not keep_data:
        print(f"{QUOTE_SYMBOL_DOING}Removing Data of {info['name']}{QUOTE_SYMBOL_DOING}")
        shutil.rmtree(os.path.join(VAR_DIR, filename))
    if os.path.exists(os.path.realpath(f"{EXEC_DIR}/desktop/{filename}.desktop")):
        print(f"{QUOTE_SYMBOL_DOING}Removing Desktop Entry{QUOTE_SYMBOL_DOING}")
        os.remove(os.path.realpath(f"{EXEC_DIR}/desktop/{filename}.desktop"))
    if "bin" in info:
        if isinstance(info["bin"], str):
            print(f"{QUOTE_SYMBOL_DOING}Removing Command {info['bin']}{QUOTE_SYMBOL_DOING}")
            bin_path = f"{EXEC_DIR}/bin/{info['bin']}"
            if os.path.islink(bin_path):
                os.unlink(bin_path)
            elif os.path.exists(bin_path):
                os.remove(bin_path)
            else:
                print(f"{QUOTE_SYMBOL_WARNING}Command not found{QUOTE_SYMBOL_WARNING}")
        elif isinstance(info["bin"], dict):
            for cmd in info["bin"].keys():
                print(f"{QUOTE_SYMBOL_DOING}Removing Command {info['bin'][cmd]}{QUOTE_SYMBOL_DOING}")
                bin_path = f"{EXEC_DIR}/bin/{info['bin'][cmd]}"
                if os.path.islink(bin_path):
                    os.unlink(bin_path)
                elif os.path.exists(bin_path):
                    os.remove(bin_path)
                else:
                    print(f"{QUOTE_SYMBOL_WARNING}Command not found{QUOTE_SYMBOL_WARNING}")


def run(filename, app_args, target: str = "run"):
    info = getpkginfo(filename)
    package_folder = os.path.join(APP_DIR, filename)
    var_folder = os.path.join(VAR_DIR, filename)
    if info is None:
        print(f"{QUOTE_SYMBOL_ERROR}Cannot find the boundaries.json file{QUOTE_SYMBOL_ERROR}")
    for k, v in PLUGINS["extends"]["run"].items():
        if not SIMPLE: print(f"{QUOTE_SYMBOL_DOING}Running Plugin {k}{QUOTE_SYMBOL_DOING}")
        v.execute(package_folder, info)
    run_command = f"APP_DIR={package_folder} VAR_DIR={var_folder} "
    run_command = run_command + os.path.realpath(os.path.join(package_folder, info["command"][target]))
    for a in app_args:
        run_command = run_command + " " + a
    os.system(run_command)


def install(filepath, ask_for_replace: bool = False):
    filepath = os.path.realpath(os.path.join(os.getcwd(), filepath))
    package_folder = os.path.join("/tmp", "boundaries")
    if os.path.exists(package_folder):
        shutil.rmtree(package_folder)
    if not os.path.isdir(filepath):
        print(f"{QUOTE_SYMBOL_DOING}Unpacking {filepath}{QUOTE_SYMBOL_DOING}")
        shutil.unpack_archive(filepath, package_folder)
    else:
        shutil.copytree(filepath, package_folder, symlinks=True)
    info_files = list(pathlib.Path(package_folder).rglob("boundaries.json"))
    if len(info_files) != 1:
        print(f"{QUOTE_SYMBOL_ERROR}pathlib did not find exactly one infofile{QUOTE_SYMBOL_ERROR}")
        return False
    package_folder = os.path.dirname(str(info_files[0].resolve()))
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
        if ask_for_replace and input(f"{QUOTE_SYMBOL_WARNING}The Package is already installed. Do you want to delete the existing one? (Y/n) ").lower() == "n":
            return False
        else:
            remove(pkg_name, True)
    shutil.move(package_folder, os.path.join(APP_DIR, pkg_name))
    package_folder = os.path.join(APP_DIR, pkg_name)
    os.chdir(package_folder)
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
    for k, v in PLUGINS["extends"]["install"].items():
        if not SIMPLE: print(f"{QUOTE_SYMBOL_DOING}Running Plugin {k}{QUOTE_SYMBOL_DOING}")
        v.execute(package_folder, info)
    if "de_name" in info:
        de_name = info["de_name"]
    else:
        de_name = pkg_name
    if "icon" in info:
        print(f"{QUOTE_SYMBOL_DOING}Creating Desktop Entry{QUOTE_SYMBOL_DOING}")
        desktop_path = os.path.realpath(f"{EXEC_DIR}/desktop/{pkg_name}.desktop")
        if "startup_wm_class" in info:
            startup_wm_class = f"\nStartupWMClass={info['startup_wm_class']}"
        else:
            startup_wm_class = ""
        with open(desktop_path, "w") as f:
            d = f"[Desktop Entry]\nName={de_name}\nExec={os.path.join(BND_DIR, 'main.py')} run \"{pkg_name}\"\nIcon={os.path.join(package_folder, info['icon'])}\nTerminal=false;\nType=Application;\nCategories=boundaries;\nStartupNotify=true;\nPath={package_folder}{startup_wm_class};"
            f.write(d)
        print(f"{QUOTE_SYMBOL_DOING}Making Desktop Entry Executable{QUOTE_SYMBOL_DOING}")
        os.system(f'chmod +x {desktop_path}')
    else:
        if not SIMPLE: print(f"{QUOTE_SYMBOL_INFO}No Icon. Not creating a .desktop File.{QUOTE_SYMBOL_INFO}")
    if "bin" in info:
        if isinstance(info["bin"], str):
            print(f"{QUOTE_SYMBOL_DOING}Creating Command {info['bin']}{QUOTE_SYMBOL_DOING}")
            binpath = os.path.realpath(f"{EXEC_DIR}/bin/{info['bin']}")
            with open(binpath, "w") as f:
                d = f'{os.path.join(BND_DIR, "main.py")} run --target \"run\" \"{pkg_name}\" $@'
                f.write(d)
            print(f"{QUOTE_SYMBOL_DOING}Making Command Executable{QUOTE_SYMBOL_DOING}")
            os.system(f'chmod +x {binpath}')
        elif isinstance(info["bin"], dict):
            for target in info["bin"].keys():
                print(f"{QUOTE_SYMBOL_DOING}Creating Command {info['bin'][target]} for target {target}{QUOTE_SYMBOL_DOING}")
                binpath = os.path.realpath(f"{EXEC_DIR}/bin/{info['bin'][target]}")
                with open(binpath, "w") as f:
                    d = f'{os.path.join(BND_DIR, "main.py")} run --target \"{target}\" \"{pkg_name}\" $@'
                    f.write(d)
                print(f"{QUOTE_SYMBOL_DOING}Making Command Executable{QUOTE_SYMBOL_DOING}")
                os.system(f'chmod +x {binpath}')
    custom_install_command_available = "install" in info["command"]
    if custom_install_command_available:
        custom_install_command = info["command"]["install"]
        if not SIMPLE:
            print(f"{QUOTE_SYMBOL_DOING}Running Command \"{custom_install_command}\"{QUOTE_SYMBOL_DOING}")
        else:
            print(f"{QUOTE_SYMBOL_DOING}Running Installation Script{QUOTE_SYMBOL_DOING}")
        custom_install_command_success = os.system(custom_install_command)
    else:
        if not SIMPLE: print(f"{QUOTE_SYMBOL_INFO}No Installation Script to run{QUOTE_SYMBOL_INFO}")
        custom_install_command_success = 0
    if custom_install_command_success != 0:
        print(f"{QUOTE_SYMBOL_ERROR}Install Command failed{QUOTE_SYMBOL_ERROR}")
        return False

    print(f"{QUOTE_SYMBOL_INFO}{pkg_name} installed successfully.{QUOTE_SYMBOL_INFO}")
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="boundaries", allow_abbrev=False, description=f"The boundaries Package Manager. Version: {VERSION}")

    parser.add_argument("--simple", help="show a Simplified Output", action="store_true")

    sub_parser = parser.add_subparsers(title="Actions", dest="action")

    install_parser = sub_parser.add_parser("install", help="Install a package")
    install_parser.add_argument("--ask", help="Ask if the Package should be replaced when it is already installed", action="store_true")
    install_parser.add_argument("path", help="Path to the Package")

    run_parser = sub_parser.add_parser("run", help="Run a package")
    run_parser.add_argument("package", help="Package Name")
    run_parser.add_argument("--target", "-t", help="Specify the Target to be run", default="run")
    run_parser.add_argument("args", help="Arguments that are passed to the Application", nargs=argparse.REMAINDER)
    remove_parser = sub_parser.add_parser("remove", help="Remove a Package")
    remove_parser.add_argument("package", help="Package Name")

    list_parser = sub_parser.add_parser("list", help="List installed Packages")

    args = parser.parse_args()
    
    SIMPLE = args.simple
    if SIMPLE:
        QUOTE_SYMBOL_DOING = QUOTE_SYMBOL_WARNING = QUOTE_SYMBOL_INFO = QUOTE_SYMBOL_ERROR = QUOTE_SYMBOL_OUTPUT = ""

    if args.action == "install":
        install(args.path, args.ask)
    elif args.action == "run":
        run(args.package, args.args, args.target)
    elif args.action == "remove":
        remove(args.package)
    elif args.action == "list":
        listpkgs()

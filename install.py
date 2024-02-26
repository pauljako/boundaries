#!/bin/python3
import os
import shutil
import sys
from pathlib import Path


def main():
    if not sys.platform == "linux":
        try:
            answer = input("Your OS is not Supported. Continue anyway? (y/N) ")
        except EOFError:
            print("EOFError When reading line. stdin might not be accessible")
            return False
        if not answer == "y":
            return False
    if os.path.exists(os.path.expanduser("~/boundaries")) and os.path.isdir(os.path.expanduser("~/boundaries")):
        try:
            answer = input("The Directory ~/boundaries already exists. Remove and Continue? (Y/n) ")
        except EOFError:
            print("EOFError When reading line. stdin might not be accessible")
            return False
        if answer == "n":
            return False
        print("Removing boundaries directory")
        shutil.rmtree(os.path.expanduser("~/boundaries"))
    print("Making sure you have git installed")
    if shutil.which("git") is None:
        print("It looks like git is not installed")
        return False
    print("Cloning boundaries...")
    os.chdir(os.path.expanduser("~"))
    if not os.system("git clone https://github.com/pauljako/boundaries.git") == 0 and os.path.exists(
            os.path.expanduser("~/boundaries")) and os.path.isdir(os.path.expanduser("~/boundaries")):
        print("Cloning failed")
        return False
    os.chdir(os.path.expanduser("~/boundaries"))
    Path("bin").symlink_to("apps/boundaries")
    Path("exec").mkdir()
    Path("exec/bin").mkdir()
    Path("exec/desktop").sysmlink_to(os.path.realpath(os.path.expanduser("~/.local/share/applications")))
    Path("var").mkdir()
    return True


if __name__ == "__main__":
    if not main():
        print("boundaries was not installed.")

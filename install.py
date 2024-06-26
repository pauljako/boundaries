#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path


def main():
    print("------------------------")
    print("| boundaries Installer |")
    print("------------------------")

    print("")

    print("=> Checking OS")
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
        print("=> Removing boundaries directory")
        shutil.rmtree(os.path.expanduser("~/boundaries"))
    print("=> Making sure you have git installed")
    if shutil.which("git") is None:
        print("It looks like git is not installed")
        return False
    print("=> Cloning boundaries")
    os.chdir(os.path.expanduser("~"))
    if not os.system("git clone https://github.com/pauljako/boundaries.git") == 0 and os.path.exists(
            os.path.expanduser("~/boundaries")) and os.path.isdir(os.path.expanduser("~/boundaries")):
        print("Cloning failed")
        return False
    os.chdir(os.path.expanduser("~/boundaries"))
    print("=> Creating Directories")
    Path("bin").symlink_to("apps/boundaries")
    Path("exec").mkdir()
    Path("exec/bin").mkdir()
    Path("exec/desktop").symlink_to(os.path.realpath(os.path.expanduser("~/.local/share/applications")))
    Path("var").mkdir()
    Path("var/boundaries").mkdir()
    print("=> Reinstalling the boundaries Package")
    os.system("apps/boundaries/main.py install apps/boundaries")

    try:
        answer = input("Do you want to add the boundaries Repository Manager (bnd-repo)? (Y/n) ")
    except EOFError:
        print("EOFError When reading line. stdin might not be accessible")
        answer = "n"
    if answer.lower() != "n":
        print("=> Cloning bnd-repo")
        os.chdir(os.path.expanduser("~"))
        clone_result = os.system("git clone https://github.com/pauljako/bnd-repo.git")
        if clone_result == 0:
            print("=> Installing the bnd-repo Package")
            os.system("boundaries/apps/boundaries/main.py install bnd-repo")
        else:
            print("Cloning failed")

    print("")
    print("boundaries successfully installed.")
    print("What to do next:")
    print("  Add the ~/boundaries/exec/bin directory to your PATH.")
    print("  You can do that using the .profile File with the following Command:")
    print("    echo 'PATH=\"$HOME/boundaries/exec/bin:$PATH\"' >> ~/.profile")

    return True


if __name__ == "__main__":
    if not main():
        print("boundaries was not installed.")

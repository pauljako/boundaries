#!/usr/bin/env bash

echo "boundaries Installer"
echo "----"
echo "Checking System"
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found and is required to use boundaries."
    echo "Aborting"
    exit 1
fi
if ! command -v bash &> /dev/null
then
    echo "bash could not be found and is required to use boundaries."
    echo "Aborting"
    exit 1
fi
if ! command -v git &> /dev/null
then
    echo "git could not be found and is required to install boundaries."
    echo "Aborting"
    exit 1
fi


ins_loc=""
loc=""

get_ins_loc() {
    echo "----"
    echo "Where do you want to install it?"
    echo "1) ~/boundaries (recommended)"
    echo "2) /opt/boundaries (system wide)"
    echo "----"
    read -r -p "> " ins_loc
    if [ "$ins_loc" = "1" ]; then
        loc="$HOME/boundaries"
    elif [ "$ins_loc" = "2" ]; then
        if [ "$UID"  = "0" ]; then
            loc="/opt/boundaries"
	    else
            echo "----"
            echo "Error. You need to run this as root"
            get_ins_loc
        fi
    else
        get_ins_loc
    fi
    if [ -d "$loc" ]; then
        echo "----"
        echo "Error. Location already exists"
        get_ins_loc
    fi

}

get_ins_loc

echo "----"
echo "boundaries will be installed into $loc"
echo "Press enter to continue"
echo "----"
read -p "> " -r con
echo "----"
mkdir -p "$loc" # &> /dev/null
if [ ! -d "$loc" ]; then
    echo "Failed to create directory"
    echo "Aborting"
    exit 1
fi
echo "Cloning into $loc"
git clone https://github.com/pauljako/boundaries.git "$loc" # &> /dev/null
echo "----"
echo "Creating Subdirectories"
mkdir -p "$loc"/var/boundaries
mkdir -p "$loc"/exec/{desktop,bin}
echo "----"
echo "Reinstalling the boundaries Core Package"
python3 "$loc"/apps/boundaries/main.py install "$loc"/apps/boundaries
echo "----"
echo "Done. You need to add the following directory to your path: $loc/exec/bin"

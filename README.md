# boundaries

Yet another useless Package Manager for Linux. It uses archives of the application and a json File containing the information that boundaries needs.

# Usage
- Installing: `boundaries --install <path to archive/dir>`
- Installing (short form): `boundaries -i <path to archive/dir>`
- Running: `boundaries --run <package name>`
- Running (short form): `boundaries -r <package name>`
- Listing Installed Packages: `boundaries --list`
- Removing: `boundaries --remove <package name>`

# Installation
### Step 1:
Install the following dependencies:

- git
- curl
- python3 (3.7+, must be in /bin/python3)
- bash (must be in /bin/bash)

Or just run one of these commands:

- Arch Linux:
`pacman -S git curl python3 bash`
- Debian / Ubuntu:
`apt install git curl python3 bash`
- Fedora:
`dnf install git curl python3 bash`

### Step 2:
Run the installer using the following command (one line):
`curl https://raw.githubusercontent.com/pauljako/boundaries/main/install.py | python3`

# Update from an older Version
Since Version 0.8.6 it is possible do directly Update boundaries. Just download the Repository and install with the following Command:

`boundaries -i <path to cloned repo>/apps/boundaries`

Press Enter if it asks if you want to replace the Exisiting one
# Status / TODO
### Repository
The Repository is in Development and a boundaries package for downloading and installing Packages using curl is available [here](https://github.com/pauljako/bnd-repo).
However, I will not host an official repository (yet), but I will really appreciate if someone does.

### Gui
Planned.

### Sandboxing
Planned for the Future.

# The boundaries.json file
The boundaries.json File is a File that contains all the Information for boundaries like name, version and much more

The File has to have at least two entries:
1. name: The name of the package. name cannot contain spaces nor uppercase letters.
2. command{run}: command is a Dictionary, which contains commands for certain things. the run command specifies the path to the executable that executes the Program.

There are many other not necessary entries. A full list can be found [here](../main/JSONFILE.md)

# Working Platforms

| Platform / OS   | Version | Status      | Notes                                         |
|-----------------|---------|-------------|-----------------------------------------------|
| macOS           | 14      | Not Working | Many Programs are not Designed for macOS      |
| NixOS           | -       | Not Working | May Work, but additional tweaking is required |
| Fedora          | 39      | Working     | -                                             |
| Arch Linux      | -       | Working     | -                                             |
| Ubuntu          | -       | Untested    | Should Work                                   |
| Debian          | 12      | Working     | -                                             |
| Raspberry Pi OS | Buster  | Working     | -                                             |

#### Please Report any issues

# Additional Info
I am not a native English speaker. Please Report Language Errors as well

# Credits
Even though I am (currently) the only contributor, I still want to Thank Google and Stack Overflow.

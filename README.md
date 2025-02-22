# boundaries

Yet another useless Package Manager for Linux. It uses archives of the application and a json File containing the information that boundaries needs.

# Usage
- Installing: `boundaries install <path to archive/dir>`
- Running: `boundaries run <package name> <arguments passed to the package>`
- Listing Installed Packages: `boundaries list`
- Removing: `boundaries remove <package name>`
- Print Help: `boundaries -h`

# Installation

Use the following Line to run the Installer (one line):
`bash <(curl -s https://raw.githubusercontent.com/pauljako/boundaries/main/install.sh)`

More information can be found [here](INSTALL.md)

# Update from an older Version
Since Version 0.8.6 it is possible do directly Update boundaries. Just download the Repository and install with the following Command:

`boundaries -i <path to cloned repo>/apps/boundaries`

Press Enter if it asks you if you want to replace the Existing one

#### Note: In Version 0.9 the CLI interface was overhauled, and you may need to Reinstall Packages so the .desktop files and the direct Command works again
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

There are many other not necessary entries. A full list can be found [here](JSONFILE.md)

# Working Platforms

| Platform / OS   | Version                   | Status      | Notes                                                  |
|-----------------|---------------------------|-------------|--------------------------------------------------------|
| NixOS           | -                         | Working     | Most packages will not work on NixOS                   |
| Fedora          | 40                        | Working     | -                                                      |
| Arch Linux      | -                         | Working     | -                                                      |
| Ubuntu          | 22.04.4 (Jammy Jellyfish) | Working     | -                                                      |
| Debian          | 12.5 (Bookworm)           | Working     | -                                                      |
| Raspberry Pi OS | 11 (Buster)               | Working     | -                                                      |
| Alpine Linux    | 3.19.1                    | Working     | /bin/python3 needs to be a Symlink to /usr/bin/python3 |
| OpenSUSE        | Tumbleweed                | Working     | -                                                      |

#### Please Report any issues

# Additional Info
I am not a native English speaker. Please Report Language Errors as well

# Credits
Even though I am (currently) the only contributor, I still want to Thank Google and Stack Overflow.

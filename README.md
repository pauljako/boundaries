# boundaries

Yet another useless Package Manager for Linux. It uses archives of the application and a json File containing the information that boundaries needs.

<h6>Note: I did not manage to get any Programs working on NixOS</h6>

# Usage
For installing an Application just run `boundaries -i <path to archive/dir>` or `boundaries --install <path to archive/dir>`.

For running an Application from the Terminal Run the following command:
`boundaries -r <app name>` or `boundaries --run <app name>`

# Installation
### Step 1:
Install the following dependencies:

- git
- curl
- python3 (3.8+)

Or just run one of these commands:

- Arch Linux:
`pacman -S git curl python3`
- Debian / Ubuntu:
`apt install git curl python3`
- Fedora:
`dnf install git curl python3`

### Step 2:
Run the installer using the following command:
`curl https://raw.githubusercontent.com/pauljako/boundaries/main/install.py | python3`
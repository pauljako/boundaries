# Installation

## Dependencies

boundaries it self only requires the following dependencies:

- `python3` (3.7+, must be in /bin/python3)
- `bash` (must be in /bin/bash)

In addition, the Install Script also requires the following dependencies:

- `git`
- `curl`

All of the above can easily be installed with one of the following commands:

- openSUSE:

```sh
zyppper install git curl python3 bash
```

- Arch Linux:

```sh
pacman -S git curl python3 bash
```

- Debian / Ubuntu:

```sh
apt install git curl python3 bash
```

- Fedora:

```sh
dnf install git curl python3 bash
```

## Using the Interactive Install Script
This is the Recommended Way of installing boundaries. It will guide you through every step of the installation.

To begin, run this in your Terminal:

```sh
bash <(curl -s https://raw.githubusercontent.com/pauljako/boundaries/main/install.sh)
```

## Using the legacy Install Script
This Script is depreceated and should'nt be used. If you however still want to use it run this:

```sh
/bin/python3 <(curl -s https://raw.githubusercontent.com/pauljako/boundaries/main/install.py)
```

## Installing Manually

1. Clone or otherwise download this Repository. It is recommended to use ~/boundaries. It will be your Installation Folder.
2. If your installation folder is not ~/boundaries, create a file called .bndpath in your home folder. It has to contain the full path to your installation folder.
3. Create the following directories in your installation folder:  `var` `exec` `exec/desktop` `exec/bin`.
4. Reinstall the boundaries Package by running the following command. `<dir>` should be replaced with your installation folder. Warnings can be ignored.
     ```sh
    /bin/python3 <dir>/apps/boundaries/main.py install <dir>/apps/boundaries
    ```

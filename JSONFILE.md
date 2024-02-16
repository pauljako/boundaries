# Options
The boundaries.json file can contain the following options:
- name: The name of the application (must be lowercase and without spaces) [required]. For Example: pycharm-ce
- command{}:
  - run: The Path to the Executable that will be the main entry for the Program [required]. For Example: bin/pycharm.sh
  - install: A Command that will be run during installation. For Example: make

- version: Specifies the Version of the Program
- icon: Path to the App icon (A .desktop Entry will not be created without it)
- de_name: The Desktop Name of the Application  (Can be uppercase and can contain spaces). For Example: PyCharm CE
- bin: When Specified a Command with the given name will be created to execute the Program Quicker

# Examples
### PyCharm CE 2023.2.1
```json
{
  "name": "pycharm-ce",
  "command": {
    "run": "bin/pycharm.sh"
  },
  "version": "2023.2.1",
  "icon": "bin/pycharm.png",
  "de_name": "PyCharm CE"
}
```
### Visual Studio Code
```json
{
    "name": "code",
    "icon": "resources/app/resources/linux/code.png",
    "command": {
        "run": "./code"
    },
    "version": "stable-x64-1702460840",
    "bin": "code",
    "de_name": "Visual Studio Code"
}
```
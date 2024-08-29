# Options
The boundaries.json file can contain the following options:
- name: The name of the application (must be lowercase and without spaces) [required]. For Example: pycharm-ce
- command{}:
  - run: The Path to the Executable that will be the main entry for the Program [required]. For Example: bin/pycharm.sh
  - install: A Command that will be run during installation. For Example: make

- version: Specifies the Version of the Program
- icon: Path to the App icon (A .desktop Entry will not be created without it)
- de_name: The Desktop Name of the Application  (Can be uppercase and can contain spaces). For Example: PyCharm CE
- bin: When Specified a Command with the given name will be created to execute the Program Quicker. Since Version 0.9.3 it can also be a dictionary for targets
- startup_wm_class: When Specified the Field StartupWMClass in the .desktop file will be set to it

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
  "de_name": "PyCharm CE",
  "startup_wm_class": "jetbrains-pycharm-ce"
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

### Go
```json
{
	"name": "golang",
	"version": "1.23.0",
	"command": {
		"run": "bin/go",
		"gofmt": "bin/gofmt"
	},
	"bin": {
		"run": "go",
		"gofmt": "gofmt"
	}
}
```
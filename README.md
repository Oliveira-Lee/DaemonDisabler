# Daemon Disabler
[中文](https://github.com/ringoju1ce/DaemonDisabler/blob/main/README_CN.md)

A tool for disabling certain daemons in iOS.

Compatible with iOS 15.7-iOS 17.7；iOS 18.0-iOS 18.1 beta 4

## Running from Source

Require:
- Python 3.8-3.11  (You can run `python3 --version` to check Python version)
- usbmuxd (only on Linux)

Note: It may be either `python`/`pip` or `python3`/`pip3` depending on your path.

### Clone the Repository
```
git clone https://github.com/ringoju1ce/DaemonDisabler.git
cd DaemonDisabler
```

### Create venv
```
python3 -m venv .venv
```

This will create a virtual environment in  `.venv` directory under the current directory.

### Activate venv (Windows)
```
.\.venv\Scripts\Activate.ps1
```

If you see `(.venv)` appear in front of your prompt, it means you have successfully activated the virtual environment. The virtual environment will deactivate when you close the current terminal or execute `deactivate` command.

If PowerShell prompts that script execution is disabled on this system, you need to run the following command with administrator privileges:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```

This will allow unsigned local scripts to run.

### Activate venv (Linux/macOS)
```
. .venv/bin/activate
```

The virtual environment will deactivate when you close the current terminal or execute `deactivate` command.

### Install Dependencies
```
pip3 install -r requirements.txt
```

### Run the Program (Command Line)
```
python3 cli_app.py
```

### Run the Program (GUI)
```
python3 gui_app.py
```

**If it can't start or isn't responding on Linux, make sure  `usbmuxd` service is running.**

**You must disable “Find My iPhone” to use this tool.**

## Building

If you want to run the program on a system without Python installed, you can build an executable with following command:
```
python3 compile.py
```

Executables will be located in `./dist` .

To compile icon resources:
```
pyrcc5 resources.qrc -o resources_rc.py
```

## Credits
- Modified from [rponeawa](https://github.com/rponeawa)/[thermalmonitordDisabler](https://github.com/rponeawa/thermalmonitordDisabler), [leminlimez](https://github.com/leminlimez)/[Nugget](https://github.com/leminlimez/Nugget)
- [JJTech](https://github.com/JJTech0130) for Sparserestore/[TrollRestore](https://github.com/JJTech0130/TrollRestore)
- [pymobiledevice3](https://github.com/doronz88/pymobiledevice3)

# Daemon Disabler

[中文](https://github.com/ringoju1ce/DaemonDisabler/blob/main/README_CN.md)

A tool for disabling certain daemons in iOS.

**Use this software at your own risk. Make a backup before using it.**

Compatible with iOS 15.7+

## Features

* Disable thermal monitor
* Disable system software update
* Disable firmware updates for accessories
* Disable unnecessary services  (UsageTrackingAgent and spotlightknowledged)

## Running the Program

**Requirements:**

* Python 3.8-3.11

**Additional requirement on Linux:**

* usbmuxd

### Clone the Repository

```
git clone https://github.com/ringoju1ce/DaemonDisabler.git
cd DaemonDisabler
```

### Create venv

```
python -m venv .venv
```

This will create a virtual environment in  `.venv` directory under the current directory.

### Activate venv (Windows)

```
.\.venv\Scripts\activate
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
pip install -r requirements.txt
```

### Run the Program (Command Line)

```
python cli_app.py
```

### Run the Program (GUI)

```
python gui_app.py
```

If it can't start or isn't responding on Linux, make sure  `usbmuxd` service is running.

## Building

If you want to run the program on a system without Python installed, you can build an executable with following command:

```
python compile.py
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

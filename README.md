# thermalmonitordDisabler
[中文](https://github.com/rponeawa/thermalmonitordDisabler/blob/main/README_CN.md)

A tool used to disable thermalmonitord to prevent throttling and screen dimming when iOS devices overheat.

Works on all versions below iOS 18.1 beta 4, may not work completely on A15+ devices.

## Running the Program
Download the latest version from [releases](https://github.com/rponeawa/thermalmonitordDisabler/releases/latest) based on your system, and run thermalmonitordDisabler or thermalmonitordDisabler.exe.

To execute the code, follow these steps:

Requirements:
- pymobiledevice3
- Python 3.8 or newer

Note: It is highly recommended to use a virtual environment:
```
python3 -m venv .env # only needed once
# macOS/Linux:  source .env/bin/activate
# Windows:      ".env/Scripts/activate.bat"
pip3 install -r requirements.txt # only needed once
python3 cli_app.py
```
Note: It may be either `python`/`pip` or `python3`/`pip3` depending on your path.

**Find My should be turned off to use this tool.**

**iPhone battery will be displayed as an unknown part/unverified in Settings after disabling thermalmonitord.**

## Credits
- Modified from [leminlimez](https://github.com/leminlimez)/[Nugget](https://github.com/leminlimez/Nugget)
- [JJTech](https://github.com/JJTech0130) for Sparserestore/[TrollRestore](https://github.com/JJTech0130/TrollRestore)
- [pymobiledevice3](https://github.com/doronz88/pymobiledevice3)

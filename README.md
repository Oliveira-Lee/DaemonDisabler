# thermalmonitordDisabler
A tool used to disable thermalmonitord to prevent throttling and screen dimming when iOS devices overheat.

## Running the Program
Requirements:
- pymobiledevice3
- Python 3.8 or newer

Note: It is highly recommended to use a virtual environment:
```
python3 -m venv .env # only needed once
# macOS/Linux:  source .env/bin/activate
# Windows:      .env/Scripts/activate.bat
pip3 install -r requirements.txt # only needed once
python3 cli_app.py
```
Note: It may be either `python`/`pip` or `python3`/`pip3` depending on your path.

## Credits
- [JJTech](https://github.com/JJTech0130) for Sparserestore/[TrollRestore](https://github.com/JJTech0130/TrollRestore)
- [pymobiledevice3](https://github.com/doronz88/pymobiledevice3)

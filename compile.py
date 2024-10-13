from sys import platform
import shutil

import PyInstaller.__main__

args = [
    'gui_app.py',
    '--hidden-import=zeroconf',
    '--hidden-import=zeroconf._utils.ipaddress',
    '--hidden-import=zeroconf._handlers.answers',
    '--onedir',
    '--name=DaemonDisabler',
    '--windowed'
]

PyInstaller.__main__.run(args)

if platform == "darwin":
    shutil.rmtree('./dist/_internal', ignore_errors=True)

from sys import platform
import shutil
import subprocess
import PyInstaller.__main__

def universal2():
    python_path = shutil.which("python3")
    arch = subprocess.run(['file', python_path], capture_output=True, text=True)
    return 'arm64' in arch.stdout and 'x86_64' in arch.stdout

args = [
    'gui_app.py',
    '--hidden-import=zeroconf',
    '--hidden-import=zeroconf._utils.ipaddress',
    '--hidden-import=zeroconf._handlers.answers',
    '--name=DaemonDisabler',
    '--windowed',
    '--noconfirm'
]

if platform == "darwin":
    args.append('--onedir')
    if universal2():
        args.append('--target-arch=universal2')
else:
    args.append('--onefile')

PyInstaller.__main__.run(args)

if platform == "darwin":
    shutil.rmtree('./dist/_internal', ignore_errors=True)
    shutil.rmtree('./dist/DaemonDisabler', ignore_errors=True)
# 守护进程禁用工具

用于禁用 iOS 系统中的一些守护进程。可以从 [Release](https://github.com/ringoju1ce/DaemonDisabler/releases/latest) 下载最新版本

**使用本软件的风险由您自行承担，使用前请备份设备**

适用于 iOS 15.7+

## 功能

* 禁用温度监测 (App 将不会在发热时主动降低运行速度;电池会显示为未知部件)
* 禁用系统更新
* 禁用配件固件更新 (Airpods等)
* 禁用其他非必要且影响性能的服务 (UsageTrackingAgent 和 spotlightknowledged)

## 运行

**需要：**

- Python 3.8-3.11

**在 Linux 上运行还需要：**

- usbmuxd

### 拉取仓库

```
git clone https://github.com/ringoju1ce/DaemonDisabler.git
cd DaemonDisabler
```

### 创建虚拟环境

```
python -m venv .venv
```

这将会在当前目录下的 `.venv` 目录中创建虚拟环境。

### 启用虚拟环境 (Windows)

```
.\.venv\Scripts\activate
```

如果您看到您的 prompt 前出现了 `(.venv)` 字样，说明您启用了虚拟环境。虚拟环境会在您关闭当前终端，或者是您执行 `deactivate` 之后关闭。在虚拟环境关闭后您需要重新启用才能运行程序。

如果 Powershell 提示您在此系统上禁止运行脚本，您需要以管理员权限执行下面的命令

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```

这将允许执行未签名的本地代码

### 启用虚拟环境 (Linux/macOS)

```
. .venv/bin/activate
```

虚拟环境会在您关闭当前终端，或者是您执行 `deactivate` 之后关闭。在虚拟环境关闭后您需要重新启用才能运行程序。

### 安装依赖

```
pip install -r requirements.txt
```

### 运行程序 (命令行)

```
python cli_app.py
```

### 运行程序 (GUI)

```
python gui_app.py
```

如果 Linux 运行报错或无响应，首先检查 usbmuxd 服务是否运行。

## 构建程序

如果您希望在没有安装 Python 环境的系统中运行程序，可以执行下面的命令构建可执行档。

```
python compile.py
```

构建的可执行档位于 `./dist`

要构建资源文件，执行下面的命令

```
pyrcc5 resources.qrc -o resources_rc.py
```

## 致谢

- 修改自 [rponeawa](https://github.com/rponeawa)/[thermalmonitordDisabler](https://github.com/rponeawa/thermalmonitordDisabler), [leminlimez](https://github.com/leminlimez)/[Nugget](https://github.com/leminlimez/Nugget)
- 感谢 [JJTech](https://github.com/JJTech0130) 提供的 Sparserestore/[TrollRestore](https://github.com/JJTech0130/TrollRestore)
- 感谢 [pymobiledevice3](https://github.com/doronz88/pymobiledevice3)

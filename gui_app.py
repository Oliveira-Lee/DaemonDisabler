import platform
import plistlib
import traceback

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtCore import QLocale
import qdarktheme
from pymobiledevice3 import usbmux
from pymobiledevice3.lockdown import create_using_usbmux

import resources_rc
from exploit.restore import restore_files, FileToRestore
from devicemanagement.constants import Device

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.device = None

        locale = QLocale.system().name()
        self.language = "zh" if locale.startswith("zh") else "en"

        self.thermalmonitord = False
        self.disable_ota = False
        self.disable_usage_tracking_agent = False
        self.disable_perfpowerservices = False

        self.language_pack = {
            "en": {
                "title": "Daemon disabler",
                "modified_by": "Modified by rponeawa from LeminLimez's Nugget.\nringojuice made a re-modified based on this.\nFree tool. If you buy this from someone, just report him.",
                "backup_warning": "Please back up your device before using!",
                "connect_prompt": "Please connect your device and try again!",
                "connected": "Connected to",
                "ios_version": "iOS",
                "apply_changes": "Applying changes to disabled.plist...",
                "applying_changes": "Applying changes...",
                "success": "Changes applied successfully!",
                "error": "An error occurred while applying changes to disabled.plist:",
                "error_connecting": "Error connecting to device",
                "goodbye": "Goodbye!",
                "input_prompt": "Enter a number: ",
                "apply_changes": "Apply Changes",
                "switch_lang": "切换到中文",
                "refresh": "Refresh",
                "menu_options": [
                    "Disable thermalmonitord",
                    "Disable OTA",
                    "Disable UsageTrackingAgent",
                    "Disable PerfPowerServices"
                ],
                "menu_options_tips": [
                    "Lock thermal state at Normal\nThis will prevent screen brightness from being reduced due to high temperatures\nRunning apps won't actively throttle performance but cannot prevent chip-level thermal throttling\nAfter disabling, the battery will show as an unknown parts",
                    "Disable services related to system updates",
                    "This service intermittently consumes a large amount of CPU\nDisabling it can significantly reduce heat during high loads and improve performance issues",
                    "This service consistently consumes a small portion of CPU usage\nDisabling it may reduce battery drain during standby"
                ]
            },
            "zh": {
                "title": "守护程序禁用工具",
                "modified_by": "由 rponeawa 基于 LeminLimez 的 Nugget 修改。\nringojuice 在此基础上进行了再次修改。\n免费工具，若您是购买而来，请举报卖家。",
                "backup_warning": "使用前请备份您的设备！",
                "connect_prompt": "请连接设备并重试！",
                "connected": "已连接到",
                "ios_version": "iOS",
                "apply_changes": "正在应用更改到 disabled.plist...",
                "applying_changes": "正在应用修改...",
                "success": "更改已成功应用！",
                "error": "应用更改时发生错误：",
                "error_connecting": "连接设备时发生错误",
                "goodbye": "再见！",
                "input_prompt": "请输入选项: ",
                "apply_changes": "应用更改",
                "switch_lang": "Switch to English",
                "refresh": "刷新",
                "menu_options": [
                    "禁用 thermalmonitord",
                    "禁用系统更新",
                    "禁用 UsageTrackingAgent",
                    "禁用 PerfPowerServices"
                ],
                "menu_options_tips": [
                    "锁定热状态为Normal\n这将防止高温导致屏幕亮度降低\nApp不会主动降低处理速度但无法阻止芯片层面的过热降频\n禁用后电池会显示未知配件",
                    "禁用系统更新相关的服务",
                    "此服务间歇性占用大量CPU\n禁用可显著降低高负载时的发热并改善卡顿情况",
                    "此服务常驻后台并稳定吃掉一小部分CPU使用率\n禁用后可减少待机时的掉电(不确定)"
                ]
            }
        }

        self.init_ui()
        self.get_device_info()

    def set_font(self):
        if platform.system() == "Windows":
            font = QtGui.QFont("Microsoft YaHei")
            QtWidgets.QApplication.setFont(font)

    def init_ui(self):
        self.setWindowTitle(self.language_pack[self.language]["title"])

        self.set_font()

        self.layout = QtWidgets.QVBoxLayout()

        self.modified_by_label = QtWidgets.QLabel(self.language_pack[self.language]["modified_by"])
        self.layout.addWidget(self.modified_by_label)

        self.icon_layout = QtWidgets.QHBoxLayout()

        self.icon_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.icon_layout.setSpacing(10)

        self.github_icon = QSvgWidget(":/brand-github.svg")
        self.github_icon.setFixedSize(24, 24)
        self.github_icon.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.github_icon.mouseReleaseEvent = lambda event: self.open_link("https://github.com/rponeawa/thermalmonitordDisabler")
        self.github_icon.setToolTip("rponeawa 的仓库地址")

        self.bilibili_icon = QSvgWidget(":/brand-bilibili.svg")
        self.bilibili_icon.setFixedSize(24, 24)
        self.bilibili_icon.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bilibili_icon.mouseReleaseEvent = lambda event: self.open_link("https://space.bilibili.com/332095459")
        self.bilibili_icon.setToolTip("rponeawa 的B站主页")

        self.icon_layout.addWidget(self.github_icon)
        self.icon_layout.addWidget(self.bilibili_icon)

        self.layout.addLayout(self.icon_layout)

        self.device_info = QtWidgets.QLabel(self.language_pack[self.language]["backup_warning"])
        self.layout.addWidget(self.device_info)

        self.thermalmonitord_checkbox = QtWidgets.QCheckBox(self.language_pack[self.language]["menu_options"][0])
        self.thermalmonitord_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][0])
        self.layout.addWidget(self.thermalmonitord_checkbox)

        self.disable_ota_checkbox = QtWidgets.QCheckBox(self.language_pack[self.language]["menu_options"][1])
        self.disable_ota_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][1])
        self.layout.addWidget(self.disable_ota_checkbox)

        self.disable_usage_tracking_checkbox = QtWidgets.QCheckBox(self.language_pack[self.language]["menu_options"][2])
        self.disable_usage_tracking_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][2])
        self.layout.addWidget(self.disable_usage_tracking_checkbox)

        self.disable_perfpowerservices_checkbox = QtWidgets.QCheckBox(self.language_pack[self.language]["menu_options"][3])
        self.disable_perfpowerservices_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][3])
        self.layout.addWidget(self.disable_perfpowerservices_checkbox)

        self.apply_button = QtWidgets.QPushButton(self.language_pack[self.language]["apply_changes"])
        self.apply_button.clicked.connect(self.apply_changes)
        self.layout.addWidget(self.apply_button)

        self.switch_language_button = QtWidgets.QPushButton(self.language_pack[self.language]["switch_lang"])
        self.switch_language_button.clicked.connect(self.switch_language)
        self.layout.addWidget(self.switch_language_button)

        self.refresh_button = QtWidgets.QPushButton(self.language_pack[self.language]["refresh"])
        self.refresh_button.clicked.connect(self.get_device_info)
        self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)
        self.show()

    def open_link(self, url):
        try:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
        except Exception as e:
            print(f"Error opening link {url}: {str(e)}")

    def get_device_info(self):
        connected_devices = usbmux.list_devices()

        if not connected_devices:
            self.device = None
            self.device_info.setText(self.language_pack[self.language]["connect_prompt"])
            self.disable_controls(True)
            return

        for current_device in connected_devices:
            if current_device.is_usb:
                try:
                    ld = create_using_usbmux(serial=current_device.serial)
                    vals = ld.all_values
                    self.device = Device(
                        uuid=current_device.serial,
                        name=vals['DeviceName'],
                        version=vals['ProductVersion'],
                        model=vals['ProductType'],
                        locale=ld.locale,
                        ld=ld
                    )
                    self.update_device_info()
                    self.disable_controls(False)
                    return
                except Exception as e:
                    self.device_info.setText(self.language_pack[self.language]["error_connecting"] + str(e))
                    print(traceback.format_exc())
                    return

        self.device = None
        self.device_info.setText(self.language_pack[self.language]["connect_prompt"])
        self.disable_controls(True)

    def disable_controls(self, disable):
        self.thermalmonitord_checkbox.setEnabled(not disable)
        self.disable_ota_checkbox.setEnabled(not disable)
        self.disable_usage_tracking_checkbox.setEnabled(not disable)
        self.disable_perfpowerservices_checkbox.setEnabled(not disable)
        self.apply_button.setEnabled(not disable)

    def update_device_info(self):
        if self.device:
            self.device_info.setText(f"{self.language_pack[self.language]['connected']} {self.device.name}\n{self.language_pack[self.language]['ios_version']} {self.device.version}")
        else:
            self.device_info.setText(self.language_pack[self.language]["connect_prompt"])
            self.disable_controls(True)

    def modify_disabled_plist(self):
        default_disabled_plist = {
            "com.apple.magicswitchd.companion": True,
            "com.apple.security.otpaird": True,
            "com.apple.dhcp6d": True,
            "com.apple.bootpd": True,
            "com.apple.ftp-proxy-embedded": False,
            "com.apple.relevanced": True
        }

        plist = default_disabled_plist.copy()

        if self.thermalmonitord_checkbox.isChecked():
            plist["com.apple.thermalmonitord"] = True
        else:
            plist.pop("com.apple.thermalmonitord", None)

        if self.disable_ota_checkbox.isChecked():
            plist["com.apple.mobile.softwareupdated"] = True
            plist["com.apple.OTATaskingAgent"] = True
            plist["com.apple.softwareupdateservicesd"] = True
        else:
            plist.pop("com.apple.mobile.softwareupdated", None)
            plist.pop("com.apple.OTATaskingAgent", None)
            plist.pop("com.apple.softwareupdateservicesd", None)

        if self.disable_usage_tracking_checkbox.isChecked():
            plist["com.apple.UsageTrackingAgent"] = True
        else:
            plist.pop("com.apple.UsageTrackingAgent", None)

        if self.disable_perfpowerservices_checkbox.isChecked():
            #plist["com.apple.PerfPowerServices"] = True
            plist["com.apple.PerfPowerServicesExtended"] = True
            #plist["com.apple.PerfPowerServicesSignpostReader"] = True
        else:
            #plist.pop("com.apple.PerfPowerServices", None)
            plist.pop("com.apple.PerfPowerServicesExtended", None)
            #plist.pop("com.apple.PerfPowerServicesSignpostReader", None)

        return plistlib.dumps(plist, fmt=plistlib.FMT_XML)

    def apply_changes(self):
        self.apply_button.setText(self.language_pack[self.language]["applying_changes"])
        self.apply_button.setEnabled(False)
        QtWidgets.QApplication.processEvents()

        QtCore.QTimer.singleShot(100, self._execute_changes)

    def _execute_changes(self):
        try:
            print("\n" + self.language_pack[self.language]["apply_changes"])
            plist_data = self.modify_disabled_plist()

            restore_files(files=[FileToRestore(
                contents=plist_data,
                restore_path="/var/db/com.apple.xpc.launchd/",
                restore_name="disabled.plist"
            )], reboot=True, lockdown_client=self.device.ld)

            QtWidgets.QMessageBox.information(self, "Success", self.language_pack[self.language]["success"])
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", self.language_pack[self.language]["error"] + str(e))
            print(traceback.format_exc())
        finally:
            self.apply_button.setText(self.language_pack[self.language]["apply_changes"])
            self.apply_button.setEnabled(True)

    def switch_language(self):
        self.language = "zh" if self.language == "en" else "en"
        self.setWindowTitle(self.language_pack[self.language]["title"])

        self.modified_by_label.setText(self.language_pack[self.language]["modified_by"])

        if self.device:
            self.update_device_info()
        else:
            self.device_info.setText(self.language_pack[self.language]["connect_prompt"])

        self.thermalmonitord_checkbox.setText(self.language_pack[self.language]["menu_options"][0])
        self.thermalmonitord_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][0])
        self.disable_ota_checkbox.setText(self.language_pack[self.language]["menu_options"][1])
        self.disable_ota_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][1])
        self.disable_usage_tracking_checkbox.setText(self.language_pack[self.language]["menu_options"][2])
        self.disable_usage_tracking_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][2])
        self.disable_perfpowerservices_checkbox.setText(self.language_pack[self.language]["menu_options"][3])
        self.disable_perfpowerservices_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][3])

        self.apply_button.setText(self.language_pack[self.language]["apply_changes"])
        self.switch_language_button.setText(self.language_pack[self.language]["switch_lang"])
        self.refresh_button.setText(self.language_pack[self.language]["refresh"])

if __name__ == "__main__":
    import sys

    qdarktheme.enable_hi_dpi()
    app = QtWidgets.QApplication(sys.argv)
    qdarktheme.setup_theme(
        additional_qss="""
        QToolTip {
            background-color: #2a2a2a;
            color: white;
            border: 1px solid white;
        }
        """
    )

    gui = App()
    sys.exit(app.exec_())
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtSvg import QSvgWidget
import qdarktheme
import platform

import resources_rc

from exploit.restore import restore_files, FileToRestore
from devicemanagement.constants import Device
from pymobiledevice3 import usbmux
from pymobiledevice3.lockdown import create_using_usbmux
import plistlib
import traceback

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.device = None
        self.language = "en"
        self.thermalmonitord = False
        self.disable_ota = False
        self.disable_usage_tracking_agent = False

        self.language_pack = {
            "en": {
                "title": "thermalmonitordDisabler",
                "modified_by": "Modified by rponeawa from LeminLimez's Nugget.\nFree tool. If you purchased it, please report the seller.",
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
                "menu_options": [
                    "Disable thermalmonitord",
                    "Disable OTA",
                    "Disable UsageTrackingAgent",
                    "Apply changes",
                    "切换到简体中文",
                    "Refresh"
                ]
            },
            "zh": {
                "title": "温控禁用工具",
                "modified_by": "由 rponeawa 基于 LeminLimez 的 Nugget 修改。\n免费工具，若您是购买而来，请举报卖家。",
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
                "menu_options": [
                    "禁用温控",
                    "禁用系统更新",
                    "禁用使用情况日志",
                    "应用更改",
                    "Switch to English",
                    "刷新"
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

        self.bilibili_icon = QSvgWidget(":/brand-bilibili.svg")
        self.bilibili_icon.setFixedSize(24, 24)
        self.bilibili_icon.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bilibili_icon.mouseReleaseEvent = lambda event: self.open_link("https://space.bilibili.com/332095459")

        self.icon_layout.addWidget(self.github_icon)
        self.icon_layout.addWidget(self.bilibili_icon)

        self.layout.addLayout(self.icon_layout)

        self.device_info = QtWidgets.QLabel(self.language_pack[self.language]["backup_warning"])
        self.layout.addWidget(self.device_info)

        self.thermalmonitord_checkbox = QtWidgets.QCheckBox(self.language_pack[self.language]["menu_options"][0])
        self.layout.addWidget(self.thermalmonitord_checkbox)

        self.disable_ota_checkbox = QtWidgets.QCheckBox(self.language_pack[self.language]["menu_options"][1])
        self.layout.addWidget(self.disable_ota_checkbox)

        self.disable_usage_tracking_checkbox = QtWidgets.QCheckBox(self.language_pack[self.language]["menu_options"][2])
        self.layout.addWidget(self.disable_usage_tracking_checkbox)

        self.apply_button = QtWidgets.QPushButton(self.language_pack[self.language]["menu_options"][3])
        self.apply_button.clicked.connect(self.apply_changes)
        self.layout.addWidget(self.apply_button)

        self.refresh_button = QtWidgets.QPushButton(self.language_pack[self.language]["menu_options"][5])
        self.refresh_button.clicked.connect(self.get_device_info)
        self.layout.addWidget(self.refresh_button)

        self.switch_language_button = QtWidgets.QPushButton(self.language_pack[self.language]["menu_options"][4])
        self.switch_language_button.clicked.connect(self.switch_language)
        self.layout.addWidget(self.switch_language_button)

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
            self.apply_button.setText(self.language_pack[self.language]["menu_options"][3])
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
        self.disable_ota_checkbox.setText(self.language_pack[self.language]["menu_options"][1])
        self.disable_usage_tracking_checkbox.setText(self.language_pack[self.language]["menu_options"][2])

        self.apply_button.setText(self.language_pack[self.language]["menu_options"][3])
        self.switch_language_button.setText(self.language_pack[self.language]["menu_options"][4])
        self.refresh_button.setText(self.language_pack[self.language]["menu_options"][5])

if __name__ == "__main__":
    import sys

    qdarktheme.enable_hi_dpi()
    app = QtWidgets.QApplication(sys.argv)
    qdarktheme.setup_theme()

    gui = App()
    sys.exit(app.exec_())

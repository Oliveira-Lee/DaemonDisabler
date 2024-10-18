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
        self.disable_spotlightknowledged = False
        self.disable_mobileaccessoryupdater = False

        self.language_pack = {
            "en": {
                "title": "Daemon disabler",
                "modified_by": "Modified by rponeawa from LeminLimez's Nugget.\nringojuice made a re-modify based on this.\nFree tool. If you buy this from someone, just report him.",
                "backup_warning": "Please back up your device before using!",
                "connect_prompt": "Please connect your device and try again!",
                "connected": "Connected to",
                "ios_version": "iOS",
                "supported": "Supported",
                "not_supported": "Not Supported",
                "apply_changes": "Applying changes to disabled.plist...",
                "applying_changes": "Applying changes...",
                "success": "Changes applied successfully!\nRemember to turn Find My back on!",
                "error": "An error occurred while applying changes:",
                "error_find_my": "\nFind My must be disabled in order to use this tool.",
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
                    "Disable spotlightknowledged",
                    "Disable MobileAccessoryUpdater(experimental)"
                ],
                "menu_options_tips": [
                    "Lock thermal state at Normal\nThis will prevent screen brightness from being reduced due to high temperatures\nRunning apps won't actively throttle performance but cannot prevent chip-level thermal throttling\nAfter disabling, the battery will show as an unknown parts",
                    "Disable services related to system updates",
                    "This service intermittently consumes a large amount of CPU\nDisabling it can significantly reduce heat during high loads and improve performance",
                    "In early versions of iOS 17, there is a bug that causes this service to use significant CPU resources\nYou don't need to disable this service when running iOS 17.5 or above\n*Disabling this service may prevent Spotlight from indexing new content",
                    "Disabling this service may prevent firmware updates for accessories (e.g. Airpods)"
                ]
            },
            "zh": {
                "title": "守护程序禁用工具",
                "modified_by": "由 rponeawa 基于 LeminLimez 的 Nugget 修改。\nringojuice 在此基础上进行了再次修改。\n免费工具，若您是购买而来，请举报卖家。",
                "backup_warning": "使用前请备份您的设备！",
                "connect_prompt": "请连接设备并重试！",
                "connected": "已连接到",
                "ios_version": "iOS",
                "supported": "支持的版本",
                "not_supported": "不支持的版本",
                "apply_changes": "正在应用更改到 disabled.plist...",
                "applying_changes": "正在应用修改...",
                "success": "更改已成功应用！\n记得重新启用查找！",
                "error": "应用更改时发生错误：",
                "error_find_my": "设备未关闭查找",
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
                    "禁用 spotlightknowledged",
                    "禁用 MobileAccessoryUpdater(实验性)"
                ],
                "menu_options_tips": [
                    "锁定热状态为Normal\n屏幕亮度不会在温度升高时降低\nApp将不会根据热状态主动降低处理速度\n*禁用此服务无法阻止芯片层面的过热降频\n*禁用后电池会显示未知部件",
                    "禁用系统更新相关的服务",
                    "此服务间歇性占用大量CPU\n禁用可显著降低高负载时的发热并改善卡顿情况",
                    "在iOS 17早期版本中, 有bug会导致此服务占用大量CPU\n如果设备分析数据中存在多条 spotlightknowledged.cpu_resource 开头的报告 说明你可能受到此问题的影响\n该问题在iOS 17.5左右被修复 如果你的 iOS 版本更高则无需禁用此项\n*禁用此服务可能会阻止 spotlight 索引新内容但不影响搜索功能",
                    "禁用此服务可能会阻止配件的固件更新(像是Airpods)"
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

        self.github_icon_r = QSvgWidget(":/brand-github.svg")
        self.github_icon_r.setFixedSize(24, 24)
        self.github_icon_r.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.github_icon_r.mouseReleaseEvent = lambda event: self.open_link("https://github.com/ringoju1ce/DaemonDisabler")
        self.github_icon_r.setToolTip("本项目的仓库地址")

        self.icon_layout.addWidget(self.github_icon)
        self.icon_layout.addWidget(self.bilibili_icon)
        self.icon_layout.addWidget(self.github_icon_r)

        self.icon_layout.addItem(QtWidgets.QSpacerItem(24, 24, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

        self.switch_language_button = QtWidgets.QPushButton()
        self.switch_language_button.setIcon(QtGui.QIcon(":/language.svg"))
        self.switch_language_button.setIconSize(QtCore.QSize(24, 24))
        self.switch_language_button.clicked.connect(self.switch_language)
        self.switch_language_button.setToolTip(self.language_pack[self.language]["switch_lang"])
        self.icon_layout.addWidget(self.switch_language_button)

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

        self.disable_spotlightknowledged_checkbox = QtWidgets.QCheckBox(self.language_pack[self.language]["menu_options"][3])
        self.disable_spotlightknowledged_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][3])
        self.layout.addWidget(self.disable_spotlightknowledged_checkbox)

        self.disable_mobileaccessoryupdater_checkbox = QtWidgets.QCheckBox(self.language_pack[self.language]["menu_options"][4])
        self.disable_mobileaccessoryupdater_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][4])
        self.layout.addWidget(self.disable_mobileaccessoryupdater_checkbox)

        self.apply_button = QtWidgets.QPushButton(self.language_pack[self.language]["apply_changes"])
        self.apply_button.clicked.connect(self.apply_changes)
        self.layout.addWidget(self.apply_button)


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
                        build=vals['BuildVersion'],
                        model=vals['ProductType'],
                        locale=ld.locale,
                        ld=ld
                    )
                    self.update_device_info()
                    if self.device.supported():
                        self.disable_controls(False)
                    else:
                        self.disable_controls(True)
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
        self.disable_spotlightknowledged_checkbox.setEnabled(not disable)
        self.disable_mobileaccessoryupdater_checkbox.setEnabled(not disable)
        self.apply_button.setEnabled(not disable)

    def update_device_info(self):
        if self.device:
            if self.device.supported():
                self.device_info.setText(f"{self.language_pack[self.language]['connected']} {self.device.name}\n{self.language_pack[self.language]['ios_version']} {self.device.version} Build {self.device.build} ({self.language_pack[self.language]['supported']})")
            else:
                self.device_info.setText(f"{self.language_pack[self.language]['connected']} {self.device.name}\n{self.language_pack[self.language]['ios_version']} {self.device.version} Build {self.device.build} ({self.language_pack[self.language]['not_supported']})")
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

        if self.disable_spotlightknowledged_checkbox.isChecked():
            plist["com.apple.spotlightknowledged"] = True
        else:
            plist.pop("com.apple.spotlightknowledged", None)

        if self.disable_mobileaccessoryupdater_checkbox.isChecked():
            plist["com.apple.accessoryupdater"] = True
            plist["com.apple.MobileAccessoryUpdater"] = True
        else:
            plist.pop("com.apple.accessoryupdater", None)
            plist.pop("com.apple.MobileAccessoryUpdater", None)

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
            error_message = str(e)
            if 'MBErrorDomain/211' in error_message:
                QtWidgets.QMessageBox.critical(self, "Error", self.language_pack[self.language]["error"] + self.language_pack[self.language]["error_find_my"])
            else:
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

        self.switch_language_button.setToolTip(self.language_pack[self.language]["switch_lang"])
        self.thermalmonitord_checkbox.setText(self.language_pack[self.language]["menu_options"][0])
        self.thermalmonitord_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][0])
        self.disable_ota_checkbox.setText(self.language_pack[self.language]["menu_options"][1])
        self.disable_ota_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][1])
        self.disable_usage_tracking_checkbox.setText(self.language_pack[self.language]["menu_options"][2])
        self.disable_usage_tracking_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][2])
        self.disable_spotlightknowledged_checkbox.setText(self.language_pack[self.language]["menu_options"][3])
        self.disable_spotlightknowledged_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][3])
        self.disable_mobileaccessoryupdater_checkbox.setText(self.language_pack[self.language]["menu_options"][4])
        self.disable_mobileaccessoryupdater_checkbox.setToolTip(self.language_pack[self.language]["menu_options_tips"][4])

        self.apply_button.setText(self.language_pack[self.language]["apply_changes"])
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
from PyQt5 import QtWidgets, QtCore
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
                "modified_by": "Modified by rponeawa from LeminLimez's Nugget",
                "backup_warning": "Please back up your device before using!",
                "connect_prompt": "Please connect your device and try again!",
                "connected": "Connected to",
                "ios_version": "iOS",
                "apply_changes": "Applying changes to disabled.plist...",
                "success": "Changes applied successfully!",
                "error": "An error occurred while applying changes to disabled.plist:",
                "goodbye": "Goodbye!",
                "input_prompt": "Enter a number: ",
                "menu_options": [
                    "1. Disable thermalmonitord",
                    "2. Disable OTA",
                    "3. Disable UsageTrackingAgent",
                    "4. Apply changes",
                    "5. Switch to Simplified Chinese",
                    "0. Exit"
                ]
            },
            "zh": {
                "title": "温控禁用工具",
                "modified_by": "由 rponeawa 基于 LeminLimez 的 Nugget 修改",
                "backup_warning": "使用前请备份您的设备！",
                "connect_prompt": "请连接设备并重试！",
                "connected": "已连接到",
                "ios_version": "iOS",
                "apply_changes": "正在应用更改到 disabled.plist...",
                "success": "更改已成功应用！",
                "error": "应用更改时发生错误：",
                "goodbye": "再见！",
                "input_prompt": "请输入选项: ",
                "menu_options": [
                    "1. 禁用温控",
                    "2. 禁用系统更新",
                    "3. 禁用日志",
                    "4. 应用更改",
                    "5. 切换到英文",
                    "0. 退出"
                ]
            }
        }

        self.init_ui()
        self.get_device_info()

    def init_ui(self):
        self.setWindowTitle(self.language_pack[self.language]["title"])
        
        self.layout = QtWidgets.QVBoxLayout()

        self.device_info = QtWidgets.QLabel(self.language_pack[self.language]["backup_warning"])
        self.layout.addWidget(self.device_info)

        self.thermalmonitord_checkbox = QtWidgets.QCheckBox(self.language_pack[self.language]["menu_options"][0])
        self.layout.addWidget(self.thermalmonitord_checkbox)

        self.disable_ota_checkbox = QtWidgets.QCheckBox(self.language_pack[self.language]["menu_options"][1])
        self.layout.addWidget(self.disable_ota_checkbox)

        self.disable_usage_tracking_checkbox = QtWidgets.QCheckBox(self.language_pack[self.language]["menu_options"][2])
        self.layout.addWidget(self.disable_usage_tracking_checkbox)

        self.apply_button = QtWidgets.QPushButton("Apply Changes")
        self.apply_button.clicked.connect(self.apply_changes)
        self.layout.addWidget(self.apply_button)

        self.switch_language_button = QtWidgets.QPushButton(self.language_pack[self.language]["menu_options"][4])
        self.switch_language_button.clicked.connect(self.switch_language)
        self.layout.addWidget(self.switch_language_button)

        self.setLayout(self.layout)
        self.show()

    def get_device_info(self):
        connected_devices = usbmux.list_devices()
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
                except Exception as e:
                    self.device_info.setText("Error connecting to device.")
                    print(traceback.format_exc())
                    return

        if self.device is None:
            self.device_info.setText("Please connect your device and try again!")

    def update_device_info(self):
        if self.device:
            self.device_info.setText(f"{self.language_pack[self.language]['connected']} {self.device.name}\n{self.language_pack[self.language]['ios_version']} {self.device.version}")

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

    def switch_language(self):
        self.language = "zh" if self.language == "en" else "en"
        self.setWindowTitle(self.language_pack[self.language]["title"])
        self.device_info.setText(self.language_pack[self.language]["backup_warning"])
        
        self.thermalmonitord_checkbox.setText(self.language_pack[self.language]["menu_options"][0])
        self.disable_ota_checkbox.setText(self.language_pack[self.language]["menu_options"][1])
        self.disable_usage_tracking_checkbox.setText(self.language_pack[self.language]["menu_options"][2])

        self.apply_button.setText(self.language_pack[self.language]["apply_changes"])
        self.switch_language_button.setText(self.language_pack[self.language]["menu_options"][4])
        self.update_device_info()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    gui = App()
    sys.exit(app.exec_())

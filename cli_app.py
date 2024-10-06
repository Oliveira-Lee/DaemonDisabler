from exploit.restore import restore_files, FileToRestore, restore_file
from tweaks.tweaks import tweaks, TweakModifyType, FeatureFlagTweak, EligibilityTweak
from devicemanagement.constants import Device

from pymobiledevice3.exceptions import PyMobileDevice3Exception
from pymobiledevice3.services.diagnostics import DiagnosticsService
from pymobiledevice3 import usbmux
from pymobiledevice3.lockdown import create_using_usbmux

from pathlib import Path
import plistlib
import traceback

running = True
device = None

while running:
    print("""\n\n\n\n
                                                                      
         ,--.                                                         
       ,--.'|                                                 ___     
   ,--,:  : |                                               ,--.'|_   
,`--.'`|  ' :         ,--,                                  |  | :,'  
|   :  :  | |       ,'_ /|  ,----._,.  ,----._,.            :  : ' :  
:   |   \\ | :  .--. |  | : /   /  ' / /   /  ' /   ,---.  .;__,'  /   
|   : '  '; |,'_ /| :  . ||   :     ||   :     |  /     \\ |  |   |    
'   ' ;.    ;|  ' | |  . .|   | .\\  .|   | .\\  . /    /  |:__,'| :    
|   | | \\   ||  | ' |  | |.   ; ';  |.   ; ';  |.    ' / |  '  : |__  
'   : |  ; .':  | : ;  ; |'   .   . |'   .   . |'   ;   /|  |  | '.'| 
|   | '`--'  '  :  `--'   \\`---`-'| | `---`-'| |'   |  / |  ;  :    ; 
'   : |      :  ,      .-./.'__/\\_: | .'__/\\_: ||   :    |  |  ,   /  
;   |.'       `--`----'    |   :    : |   :    : \\   \\  /    ---`-'   
'---'                       \\   \\  /   \\   \\  /   `----'              
                             `--`-'     `--`-'                        
    """)
    print("CLI v2.2")
    print("by LeminLimez, modified by @rponeawa")
    print("Please back up your device before using!")

    while device == None:
        connected_devices = usbmux.list_devices()
        for current_device in connected_devices:
            if current_device.is_usb:
                try:
                    ld = create_using_usbmux(serial=current_device.serial)
                    vals = ld.all_values
                    device = Device(uuid=current_device.serial, name=vals['DeviceName'], version=vals['ProductVersion'], model=vals['ProductType'], locale=ld.locale, ld=ld)
                except Exception as e:
                    print(traceback.format_exc())
                    input("Press Enter to continue...")
        
        if device == None:
            print("Please connect your device and try again!")
            input("Press Enter to continue...")

    print(f"Connected to {device.name}\niOS {device.version}\n")
    
    print("1. Disable thermalmonitord")
    print("0. Exit\n")
    page = int(input("Enter a number: "))
    
    if page == 1:
        try:
            print("Attempting to restore disabled.plist...")
            restore_files(files=[FileToRestore(
                contents=b"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>com.apple.magicswitchd.companion</key>
	<true/>
	<key>com.apple.security.otpaird</key>
	<true/>
	<key>com.apple.dhcp6d</key>
	<true/>
	<key>com.apple.bootpd</key>
	<true/>
	<key>com.apple.ftp-proxy-embedded</key>
	<false/>
	<key>com.apple.relevanced</key>
	<true/>
	<key>com.apple.thermalmonitord</key>
	<true/>
</dict>
</plist>""",                         
                restore_path="/var/db/com.apple.xpc.launchd/",
                restore_name="disabled.plist"
            )], reboot=True, lockdown_client=device.ld)
            
            print("disabled.plist restored successfully!")
        except Exception as e:
            print("An error occurred while restoring disabled.plist:")
            print(traceback.format_exc())
            
        running = False

    elif page == 0:
        print("Goodbye!")
        running = False
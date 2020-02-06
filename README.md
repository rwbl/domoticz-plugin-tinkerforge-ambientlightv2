# domoticz-plugin-tinkerforge-ambientlightv2
[Domoticz](https://www.domoticz.com/) plugin to interact with the [Tinkerforge Ambient Light Bricklet 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Ambient_Light_V2.html#ambient-light-v2-bricklet).

# Objectives
* To read the illuminance of the Tinkerforge Ambient Light Bricklet 2.0.
* To learn how to write generic Python plugin(s) for the Domoticz Home Automation system communicating with [Tinkerforge](http://www.tinkerforge.com) Building Blocks. This plugin espcially focus on using the Domoticz Hearbeat.

**NOTE**: The Ambient Light Bricklet 2.0 is discontinued and is no longer sold. The Ambient Light Bricklet 3.0 is the recommended replacement.

_Abbreviations_: TF=Tinkerforge, Bricklet=Tinkerforge Ambient Light Bricklet 2.0, GUI=Domoticz Web UI.

## Solution
A Domoticz Python plugin named "Tinkerforge Ambient Light Bricklet 2.0" gets in regular polling intervals the illuminance.
The Domoticz device created is from Type: Lux, SubType: Lux.
The bricklet is connected to a Tinkerforge Master Brick which is direct connected via USB with the Domoticz Home Automation system.
The Domoticz Home Automation system is running on a Raspberry Pi 3B+.

### Logic
The only function of the plugin is to get the illuminance measured (Lux) from the bicklet and update the Domoticz device (Lux).
This is triggered by the plugin polling interval (s) parameter based on the Domoticz default heartbeat (every 10s).
The action taken is: IP connection > Create device object > get the illuminance & update Domoticz device > IP disconnect.

If "(HeartbeatCounter x HeartbeatInterval ) % PollingInterval = 0" then the illuminance is read & updated.
* HeartbeatCounter - increases every 10s heartbeat
* HeartbeatInterval - 10s
* PollingIntervaland - plugin parameter (default 300s = 5 min)

Examples trigger action:
* every minute (60s = 6 x 10s heartbeats] = (6 x 10) % 60 = 0
* every 5 minutes (300s = 30 x 10s heartbeats] = (30 x 10) % 300 = 0

Any additional logic to be defined in Domoticz. Either by additional devices or scripts.
Examples
* Switch light(s) on, if illuminance below certain threshold.
More see section "dzVents Lua Automation Script Examples".

## Hardware Parts
* Raspberry Pi 3B+ [(Info)](https://www.raspberrypi.org)
* Tinkerforge Master Brick 2.1 FW 2.4.10 [(Info)](https://www.tinkerforge.com/en/doc/Hardware/Bricks/Master_Brick.html#master-brick)
* Tinkerforge Ambient Light Bricklet 2.0 FW 2.0.2 [(Info)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Ambient_Light_V2.html#ambient-light-v2-bricklet)

## Software
* Raspberry Pi Raspian Debian Linux Buster 4.19.93-v7+ #1290
* Domoticz Home Automation System V4.11717 (beta) 
* Tinkerforge Brick Daemon 2.4.1, Brick Viewer 2.4.11
* Tinkerforge Python API-Binding 2.1.24 [(Info)](https://www.tinkerforge.com/en/doc/Software/Bricklets/AmbientLightV2_Bricklet_Python.html#ambient-light-v2-bricklet-python-api)
* Python 3.7.3, GCC 8.2.0
* The versions for developing this plugin are subject to change.

## Quick Steps
For implementing the Plugin on the Domoticz Server running on the Raspberry Pi.
See also Python Plugin Code (well documented) **plugin.py**.

## Test Setup
For testing this plugin, the test setup has a Master Brick with Ambient Light Bricklet 2.0 connected to port C.
On the Raspberry Pi, it is mandatory to install the Tinkerforge Brick Daemon and Brick Viewer following [these](https://www.tinkerforge.com/en/doc/Embedded/Raspberry_Pi.html) installation instructions (for Raspian armhf).
Start the Brick Viewer and action:
* Update the devices firmware
* Obtain the UID of the RGB LED Bricklet 2.0 as required by the plugin (i.e. Jng).

## Domoticz Web GUI
Open windows GUI Setup > Hardware, GUI Setup > Log, GUI Setup > Devices
This is required to add the new hardware with its device and monitor if the plugin code is running without errors.
It is imporant, that the GUI > Setup > Hardware accepts new devices!

## Create folder
The folder name is the same as the key property of the plugin (i.e. plugin key="TFAMBIENTLIGHTLV2").
```
cd /home/pi/domoticz/plugins/TFAMBIENTLIGHTLV2
```

## Create the plugin
The plugin has a mandatory filename **plugin.py** located in the created plugin folder.
Domoticz Python Plugin Source Code: see file **plugin.py**.

## Install the Tinkerforge Python API
There are two options.

### 1) sudo pip3 install tinkerforge
Advantage: in case of binding updates, only a single folder must be updated.
Check if a subfolder tinkerforge is created in folder /usr/lib/python3/dist-packages.
**Note**
Check the version of "python3" in the folder path. This could also be python 3.7 or other = see below.

**If for some reason the bindings are not installed**
Unzip the Tinkerforge Python Binding into the folder /usr/lib/python3/dist-packages.
_Example_
Create subfolder Tinkerforge holding the Tinkerforge Python Library
```
cd /home/pi/tinkerforge
```
Unpack the latest python bindings into folder /home/pi/tinkerforge
Copy /home/pi/tinkerforge to the Python3 dist-packges
```
sudo cp -r /home/pi/tinkerforge /usr/lib/python3/dist-packages/
```

In the Python Plugin code amend the import path to enable using the Tinkerforge libraries
```
from os import path
import sys
sys.path
sys.path.append('/usr/local/lib/python3.7/dist-packages')
```

### 2) Install the Tinkerforge Python Bindings in a subfolder of the plugin and copy the binding content.
Disadvantage: Every Python plugin using the Tinkerforge bindings must have a subfolder tinkerforge.
In case of binding updates,each of the tinkerforge plugin folders must be updated.
/home/pi/domoticz/plugins/soilmoisturemonitor/tinkerforge

There is no need to amend the path as for option 1.

For either ways, the bindings are used like:
```
import tinkerforge
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ambient_light_v2 import BrickletAmbientLightV2
```
**Note**
Add more bindings depending Tinkerforge bricks & bricklets used.

Ensure to update the files in case of newer Tinkerforge Python Bindings.

## Make plugin.py executable
```
cd /home/pi/domoticz/plugins/TFAMBIENTLIGHTLV2
chmod +x plugin.py
```

## Restart Domoticz
Restart Domoticz to find the plugin:
```
sudo systemctl restart domoticz.service
```

**Note**
When making changes to the Python plugin code, ensure to restart Domoticz and refresh any of the Domoticz Web GUI's.

## Domoticz Add Hardware Tinkerforge Ambient Light Bricklet 2.0
**IMPORTANT**
Prior adding, set GUI Stup > Settings > Hardware the option to allow new hardware.
If this option is not enabled, no new devices are created assigned to this hardware.
Check in the Domoticz log as error message Python script at the line where the new device is used
(i.e. Domoticz.Debug("Device created: "+Devices[1].Name))

In the GUI Setup > Hardware add the new hardware "Tinkerforge Ambient Light Bricklet 2.0".

## Add Hardware - Check the Domoticz Log
After adding,ensure to check the Domoticz Log (GUI Setup > Log)

## Example Domoticz Log Entry Adding Hardware with Debug=True
```
2020-02-06 10:55:15.156 (TFALV2) Debug logging mask set to: PYTHON PLUGIN QUEUE IMAGE DEVICE CONNECTION MESSAGE ALL 
2020-02-06 10:55:15.156 (TFALV2) 'HardwareID':'8' 
2020-02-06 10:55:15.156 (TFALV2) 'HomeFolder':'/home/pi/domoticz/plugins/TFAMBIENTLIGHTLV2/' 
2020-02-06 10:55:15.156 (TFALV2) 'StartupFolder':'/home/pi/domoticz/' 
2020-02-06 10:55:15.156 (TFALV2) 'UserDataFolder':'/home/pi/domoticz/' 
2020-02-06 10:55:15.156 (TFALV2) 'Database':'/home/pi/domoticz/domoticz.db' 
2020-02-06 10:55:15.156 (TFALV2) 'Language':'en' 
2020-02-06 10:55:15.156 (TFALV2) 'Version':'1.0.0' 
2020-02-06 10:55:15.156 (TFALV2) 'Author':'rwbL' 
2020-02-06 10:55:15.156 (TFALV2) 'Name':'TFALV2' 
2020-02-06 10:55:15.156 (TFALV2) 'Address':'127.0.0.1' 
2020-02-06 10:55:15.156 (TFALV2) 'Port':'4223' 
2020-02-06 10:55:15.156 (TFALV2) 'Key':'TFAMBIENTLIGHTLV2' 
2020-02-06 10:55:15.156 (TFALV2) 'Mode1':'yyc' 
2020-02-06 10:55:15.156 (TFALV2) 'Mode5':'60' 
2020-02-06 10:55:15.156 (TFALV2) 'Mode6':'Debug' 
2020-02-06 10:55:15.156 (TFALV2) 'DomoticzVersion':'4.11670' 
2020-02-06 10:55:15.156 (TFALV2) 'DomoticzHash':'f6af0fa0c' 
2020-02-06 10:55:15.156 (TFALV2) 'DomoticzBuildTime':'2020-02-02 12:21:53' 
2020-02-06 10:55:15.156 (TFALV2) Device count: 0 
2020-02-06 10:55:15.156 (TFALV2) Creating new Device 
2020-02-06 10:55:15.156 (TFALV2) Creating device 'Ambient Light'. 
2020-02-06 10:55:15.157 (TFALV2) Device created: TFALV2 - Ambient Light 
2020-02-06 10:55:15.157 (TFALV2) SetBrickletConfiguration 
2020-02-06 10:55:15.153 Status: (TFALV2) Entering work loop. 
2020-02-06 10:55:15.154 Status: (TFALV2) Initialized version 1.0.0, author 'rwbL'
```

## Example Heartbeat Polling with Debug ON
```
2020-02-06 10:58:15.199 (TFALV2) onHeartbeat called. Counter=180 (Heartbeat=60) 
2020-02-06 10:58:15.199 (TFALV2) GetBrickletIlluminance: Unit 1, ID=80 
2020-02-06 10:58:15.209 (TFALV2 - Ambient Light) Updating device from 0:'93.86' to have values 0:'99.38'. 
2020-02-06 10:58:15.338 (TFALV2) GetBrickletIlluminance: OK 
```
## Example Heartbeat Polling with Debug OFF
Heartbeat every minute.
```
2020-02-06 11:30:28.561 (TFALV2) Illuminance updated: 147.81 
2020-02-06 11:31:28.562 (TFALV2) Illuminance updated: 150.28 
2020-02-06 11:32:28.602 (TFALV2) Illuminance updated: 158.44 
2020-02-06 11:33:28.596 (TFALV2) Illuminance updated: 179.66
```

## Example Heartbeat change from 60 to 300s [Mode5]
```
2020-02-06 11:00:42.459 (TFALV2) Debug logging mask set to: PYTHON PLUGIN QUEUE IMAGE DEVICE CONNECTION MESSAGE ALL 
2020-02-06 11:00:42.459 (TFALV2) 'HardwareID':'8' 
2020-02-06 11:00:42.459 (TFALV2) 'HomeFolder':'/home/pi/domoticz/plugins/TFAMBIENTLIGHTLV2/' 
2020-02-06 11:00:42.459 (TFALV2) 'StartupFolder':'/home/pi/domoticz/' 
2020-02-06 11:00:42.459 (TFALV2) 'UserDataFolder':'/home/pi/domoticz/' 
2020-02-06 11:00:42.459 (TFALV2) 'Database':'/home/pi/domoticz/domoticz.db' 
2020-02-06 11:00:42.459 (TFALV2) 'Language':'en' 
2020-02-06 11:00:42.459 (TFALV2) 'Version':'1.0.0' 
2020-02-06 11:00:42.459 (TFALV2) 'Author':'rwbL' 
2020-02-06 11:00:42.459 (TFALV2) 'Name':'TFALV2' 
2020-02-06 11:00:42.459 (TFALV2) 'Address':'127.0.0.1' 
2020-02-06 11:00:42.459 (TFALV2) 'Port':'4223' 
2020-02-06 11:00:42.459 (TFALV2) 'Key':'TFAMBIENTLIGHTLV2' 
2020-02-06 11:00:42.459 (TFALV2) 'Mode1':'yyc' 
2020-02-06 11:00:42.459 (TFALV2) 'Mode5':'300' 
2020-02-06 11:00:42.459 (TFALV2) 'Mode6':'Debug' 
2020-02-06 11:00:42.459 (TFALV2) 'DomoticzVersion':'4.11670' 
2020-02-06 11:00:42.459 (TFALV2) 'DomoticzHash':'f6af0fa0c' 
2020-02-06 11:00:42.459 (TFALV2) 'DomoticzBuildTime':'2020-02-02 12:21:53' 
2020-02-06 11:00:42.459 (TFALV2) Device count: 1 
2020-02-06 11:00:42.459 (TFALV2) Device: 1 - ID: 80, Name: 'TFALV2 - Ambient Light', nValue: 0, sValue: '112.76' 
2020-02-06 11:00:42.460 (TFALV2) Device ID: '80' 
2020-02-06 11:00:42.460 (TFALV2) Device Name: 'TFALV2 - Ambient Light' 
2020-02-06 11:00:42.460 (TFALV2) Device nValue: 0 
2020-02-06 11:00:42.460 (TFALV2) Device sValue: '112.76' 
2020-02-06 11:00:42.460 (TFALV2) Device LastLevel: 0 
2020-02-06 11:00:42.460 (TFALV2) SetBrickletConfiguration
```

## dzVents Lua Automation Script Examples

### Switch Light if Lux below threshold (dzVents Lua Automation Script)
This example runs the plugin on a Domoticz Development System (Ambient Light Bricklet 2.0 > Master Brick > Raspberry Pi 3B+).
If the measured Ambient Light Lux value is below a threshold, as set by a user variable, a Hue light, connected to a Domoticz Production System, is turned ON.
If the value is above threshold, the light is turned OFF again.
```
-- Tinkerforge Ambient Light Bricklet 2.0 Plugin - Test Script 
-- dzVents Automation Script: tfalv2_light_control
-- Switch light(s) if the measued lux value is below threshold.
-- The threshold is set by the user variable TH_AMBIENTLIGHT (Integer)
local DOMOTICZURL = 'http://rpi-domoticz-ip:8080'
-- Parameter On | Off
local REQUESTURL = DOMOTICZURL .. '/json.htm?type=command&param=switchlight&idx=118&switchcmd='

-- NOT USED for now
-- ensure the httpResponse name is unique across all dzVents scripts!
-- use the scriptname plus Callback
local HTTPCALLBACKNAME = 'RESTFALV2LIGHTCONTROL'

-- idx of the devices
local IDXAMBIENTLIGHT = 80         -- Type=Lux,Lux
local IDXHUEMAKELAB = 118          -- Type=Light/Switch,Switch,Dimmer

-- idx of the user variables (TH= threshold)
local IDXTHAMBIENTLIGHT = 1   -- Type:Integer

return {
	on = {
		devices = {
			IDXAMBIENTLIGHT
		}
	},
    data = {
        -- keep the light state
        lightstate = { initial = 0 }
   },

	execute = function(domoticz, device)
		-- domoticz.log('Device ' .. device.name .. ' was changed', domoticz.LOG_INFO)

        -- get the threshold from the user variable
        local threshold = domoticz.variables(IDXTHAMBIENTLIGHT).value

        -- switch light if the threshold > 0
        if threshold > 0 then
            -- switch the Light On
	    	if domoticz.devices(IDXAMBIENTLIGHT).lux <= threshold and domoticz.data.lightstate == 0 then
                domoticz.openURL(REQUESTURL .. 'On')
                domoticz.data.lightstate = 1
    		end

            -- switch the Light Off
		    if domoticz.devices(IDXAMBIENTLIGHT).lux > threshold and domoticz.data.lightstate == 1 then
                domoticz.openURL(REQUESTURL .. 'Off')
                domoticz.data.lightstate = 0
		    end
            
        end

	end
}
```

#### Example Log
```
2020-02-06 11:50:28.809 (TFALV2) Illuminance updated: 182.48 
2020-02-06 11:50:28.886 Status: dzVents: Info: Handling events for: "TFALV2 - Ambient Light", value: "182.48" 
2020-02-06 11:50:28.886 Status: dzVents: Info: ------ Start internal script: tfalv2_light_control: Device: "TFALV2 - Ambient Light (TFALV2)", Index: 80 
2020-02-06 11:50:28.889 Status: dzVents: Info: ------ Finished tfalv2_light_control 
```

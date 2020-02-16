# Domoticz Home Automation - Plugin Tinkerforge Ambient Light Bricklet 2.0
# @author Robert W.B. Linn
# @version 1.0.0 (Build 20200207)
#
# NOTE: after every change run
# sudo chmod +x *.*                      
# sudo systemctl restart domoticz.service OR sudo service domoticz.sh restart
#
# Domoticz Python Plugin Development Documentation:
# https://www.domoticz.com/wiki/Developing_a_Python_plugin
# Tinkerforge Ambient Light Bricklet 2.0 Documentation:
# Hardware:
# https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Ambient_Light_V2.html#ambient-light-v2-bricklet
# API Python Documentation:
# https://www.tinkerforge.com/en/doc/Software/Bricklets/AmbientLightV2_Bricklet_Python.html#ambient-light-v2-bricklet-python-api

"""
<plugin key="tfambientlightlv2" name="Tinkerforge Ambient Light Bricklet 2.0" author="rwbL" version="1.0.0">
    <description>
        <h2>Tinkerforge Ambient Light 2.0</h2><br/>
        This bricklet measures in regular intervals, the ambient light in lux.<br/>
        The Domoticz device created is from Type: Lux, SubType: Lux.<br/>
        <br/>
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>Address: IP address of the host connected to. Default: 127.0.0.1 (for USB connection)</li>
            <li>Port: Port used by the host. Default: 4223</li>
            <li>UID: Unique identifier of Ambient Light Bricklet 2.0. Obtain the UID via the Brick Viewer. Default: yyc</li>
            <li>Polling: Regular interval to measure lux in s. Default: 300 (every 5 minutes)</li>
        </ul>
    </description>
    <params>
        <param field="Address" label="Host" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="Port" width="75px" required="true" default="4223"/>
        <param field="Mode1" label="UID" width="200px" required="true" default="yyc"/>
        <param field="Mode5" label="Polling" width="75px" required="true" default="300"/>
        <param field="Mode6" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug" default="true"/>
                <option label="False" value="Normal"/>
            </options>
        </param>
    </params>
</plugin>
""" 

## Imports
import Domoticz
import urllib
import urllib.request

# Amend the import path to enable using the Tinkerforge libraries
# Alternate (ensure to update in case newer Python API bindings):
# create folder tinkerforge and copy the binding content, i.e.
# /home/pi/domoticz/plugins/TFAMBIENTLIGHTV2
from os import path
import sys
sys.path
sys.path.append('/usr/local/lib/python3.7/dist-packages')

import tinkerforge
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ambient_light_v2 import BrickletAmbientLightV2

# Units
UNITILLUMINATION = 1
# Device Status Level & Text
STATUSLEVELOK = 1
STATUSLEVELERROR = 5
STATUSTEXTOK = "OK"
STATUSTEXTERROR = "ERROR"

class BasePlugin:

    def __init__(self):
        self.Debug = False
        
        # The Domoticz heartbeat is set to every 10 seconds. Do not use a higher value than 30 as Domoticz message "Error: hardware (N) thread seems to have ended unexpectedly"
        # The plugin heartbeat is set in Parameter.Mode5 (seconds). This is determined by using a hearbeatcounter which is triggered by:
        # (self.HeartbeatCounter * self.HeartbeatInterval) % int(Parameter.Mode5) = 0
        # Example: trigger action every 60s [every 6 heartbeats] = (6 * 10) mod 60 = 0 or every 5 minutes (300s) [every 30 heartbeats] = (30 * 10) mod 300 = 0
        self.HeartbeatInterval = 10
        self.HeartbeatCounter = 0

    def onStart(self):
        Domoticz.Debug("onStart called")
        Domoticz.Debug("Debug Mode:" + Parameters["Mode6"])
        if Parameters["Mode6"] == "Debug":
            self.debug = True
            Domoticz.Debugging(1)
            DumpConfigToLog()

        if (len(Devices) == 0):
            # Create new devices for the Hardware = each channel is a dimmer switch
            Domoticz.Debug("Creating new Device")
            Domoticz.Device(Name="Ambient Light", Unit=UNITILLUMINATION, TypeName="Illumination", Used=1).Create()
            Domoticz.Debug("Device created: "+Devices[UNITILLUMINATION].Name)

        # Get the UID of the bricklet
        if len(Parameters["Mode1"]) == 0:
            StatusToLog(STATUSLEVELERROR, "[ERROR] Device UID not set. Get the UID using the Brick Viewer.")
            return

        # Set the bricklet configuration
        SetBrickletConfiguration()

    def onStop(self):
        Domoticz.Debug("Plugin is stopping.")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Debug("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level) + "', Hue: " + str(Hue))

    def onDeviceModified(self, Unit):
        Domoticz.Debug("onDeviceModified called: Unit " + str(Unit))
        # Domoticz.Debug("nValue="+str(Devices[Unit].nValue) + ",sValue="+Devices[Unit].sValue + ", Color RGB="+Devices[Unit].Color)

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Debug("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Debug("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Debug("onHeartbeat called")
        # NOT USED = PLACEHOLDER
        self.HeartbeatCounter = self.HeartbeatCounter + 1
        Domoticz.Debug("onHeartbeat called. Counter=" + str(self.HeartbeatCounter * self.HeartbeatInterval) + " (Heartbeat=" + Parameters["Mode5"] + ")")
        # check the heartbeatcounter against the heartbeatinterval
        if (self.HeartbeatCounter * self.HeartbeatInterval) % int(Parameters["Mode5"]) == 0:
            try:
                SetBrickletIlluminance(UNITILLUMINATION)
                return
            except:
                #Domoticz.Error("[ERROR] ...")
                return

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onDeviceModified(Unit):
    global _plugin
    _plugin.onDeviceModified(Unit)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

# Tinkerforge Bricklet

# Set the bricklet configuration
# NOT SUPPORTED = Status LED = OFF - use newer bricklet v3 - kept this function as PLACEHOLDER
def SetBrickletConfiguration():
    Domoticz.Debug("SetBrickletConfiguration")
    """
    try:
        # Create IP connection
        ipConn = IPConnection()
        # Create device object
        alDev = BrickletAmbientLightV2(Parameters["Mode1"], ipConn)
        # Connect to brickd using Host and Port
        ipConn.connect(Parameters["Address"], int(Parameters["Port"]))
        # Update the configuration
        alDev...
        # Disconnect
        ipConn.disconnect()
        Domoticz.Debug("SetBrickletConfiguration OK")
    except:
        Domoticz.Error("[ERROR] SetBrickletConfiguration failed. Check bricklet.")
    return
    """

# Get the illuminance of the bricklet
def SetBrickletIlluminance(Unit):
    Domoticz.Debug("GetBrickletIlluminance: Unit " + str(Unit) + ", ID="+str(Devices[Unit].ID) )
    try:
        # Create IP connection
        ipConn = IPConnection()
        # Create device object
        alDev = BrickletAmbientLightV2(Parameters["Mode1"], ipConn)
        # Connect to brickd using Host and Port
        ipConn.connect(Parameters["Address"], int(Parameters["Port"]))
        # Get current illuminance
        illuminance = alDev.get_illuminance()
        if illuminance > 0:
            illuminance = illuminance/100.0
        Devices[Unit].Update( nValue=0, sValue=str(illuminance) )
        Domoticz.Log("Illuminance updated: "+str(illuminance))
        # Disconnect
        ipConn.disconnect()
        Domoticz.Debug("GetBrickletIlluminance: OK")
    except:
        Domoticz.Error("[ERROR] SetBrickletIlluminance failed. Check bricklet.")
    return illuminance

# Generic helper functions

# Dump the plugin parameter & device information to the domoticz debug log
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

# Log a status message, either to the domoticz log or error
# Alert Level: 1=OK, 4=ERROR
def StatusToLog(level,text):
    if level == STATUSLEVELOK:
        Domoticz.Log(text)
    if level == STATUSLEVELERROR:
        Domoticz.Error(text)
    return

# Map a range from to.
# Example mapping 0-100% to 0-255: MapRange(255,0,100,0,255) gives 255.
def MapRange(x,a,b,c,d):
    try:
        y=(x-a)/(b-a)*(d-c)+c
    except:
        y=-1
    return round(y)
   

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

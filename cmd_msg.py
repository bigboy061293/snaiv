from pymavlink import mavutil
from pymavlink.dialects.v20 import ardupilotmega as mavlink2
import radars_mama
def setWaypointSpeed(whichMavlink, waypointSpeed):
	whichMavlink.mav.command_long_send(whichMavlink.target_system, whichMavlink.target_component,
				mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED, 0,
				0, waypointSpeed / 100, -1, 0,0,0,0)
            
def setLoiterAccelerate(whichMavlink,loiterAccelerate):
    #while True:
        whichMavlink.mav.param_set_send(
            whichMavlink.target_system, whichMavlink.target_component,
            b'LOIT_ACC_MAX',
            int(loiterAccelerate),
            mavutil.mavlink.MAV_PARAM_TYPE_UINT16)
def setLoiterSpeed(whichMavlink,loiterSpeed):
    #while True:
        whichMavlink.mav.param_set_send(
            whichMavlink.target_system, whichMavlink.target_component,
            b'LOIT_SPEED',
            int(loiterSpeed),
            mavutil.mavlink.MAV_PARAM_TYPE_UINT16)

def sendMessageDistanceSensor(whichMavlink,distance, place):
    
    if distance in range(radars_mama.radarMinRange, radars_mama.radarMaxRange):
        msss = mavlink2.MAVLink_distance_sensor_message(
                        0, #time
                        radars_mama.radarMinRange, #min distance
                        radars_mama.radarMaxRange, #max distance
                        distance, # current
                        3, #type
                        1, #id
                        place, #ori
                        255)
        
        whichMavlink.mav.send(msss)
    
    else:
        return
    
def sendMessageDistanceSensor_RC9(whichMavlink,pulse):
	UINT16_MAX = 65535
	mss = mavlink2.MAVLink_rc_channels_override_message(
					0,
					0,
					UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, 
					pulse, 
					UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX)
	whichMavlink.mav.send(mss)

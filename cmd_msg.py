from pymavlink import mavutil

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

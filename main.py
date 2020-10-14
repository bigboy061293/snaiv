from common_import import *
#import psutil
common_vars.linkAP = mavutil.mavlink_connection(VIANS_DATALINK_MODULE, dialect = "ardupilotmega")

establish_link.connectVianS(common_vars.linkAP)
input_output.initializeJNIO()

	
_updateTelemetry = common_vars.updateTelemetry(1, "Tele")
_updateTelemetry.start()
_updateWaypoint = common_vars.updateWaypoint(2, 'ms')
_readRadarThree = radars_mama.readRadarThree(3, 'rd')
_readRadarThree.start()
_keyboardInput = input_output.keyboardInput(4, 'io')
_keyboardInput.start()


_updateProcess = radars_mama.updateProcess(5,'pc')
_updateProcess.start()

_radarCounter = radars_mama.radarCounter(6, 'ct')
_radarCounter.start()
_pumpControl = input_output.pumpControl(7,'pcc')
_pumpControl.start()
_logging = log_record.logging(8,'lg')
_logging.start()
"""
_updateTelemetry.pause()

_updateWaypoint = common_vars.updateWaypoint(2, 'ms')
_updateWaypoint.start()
time.sleep(1)
_updateWaypoint.pause()
"""
while True:

	#cmd_msg.setWaypointSpeed(common_vars.linkAP, 1000)
	
	if input_output.keyIp == 'load mission':
		input_output.keyIp = ''
		_updateTelemetry.pause()
		_updateWaypoint.start()
		time.sleep(1)
		_updateWaypoint.pause()
		_updateTelemetry.resume()
		print common_vars.vianSMissionList
	elif input_output.keyIp[0:8] == 'wpspeed,':
		input_output.keyIp = ''
		print 'sw change'
		
	pass
	
	
	


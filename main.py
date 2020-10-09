from common_import import *


common_vars.linkAP = mavutil.mavlink_connection(VIANS_DATALINK_MODULE, dialect = "ardupilotmega")

establish_link.connectVianS(common_vars.linkAP)

	
_updateTelemetry = common_vars.updateTelemetry(1, "Tele")
_updateTelemetry.start()
_updateTelemetry.pause()

_updateWaypoint = common_vars.updateWaypoint(2, 'ms')
_updateWaypoint.start()
time.sleep(1)
_updateWaypoint.pause()

_readRadarThree = radars_mama.readRadarThree(3, 'rd')
_readRadarThree.start()
_updateProcess = radars_mama.updateProcess(4,'pc')
_updateProcess.start()
while True:
	#print common_vars.vianSGNSS
	time.sleep(0.5)
	pass
	
	
	


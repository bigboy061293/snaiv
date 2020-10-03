from common_import import *


common_vars.linkAP = mavutil.mavlink_connection(VIANS_DATALINK_MODULE, dialect = "ardupilotmega")

common_vars.vianSAlt = 10
print common_vars.vianSAlt
	
_updateTelemetry = common_vars.updateTelemetry(1, "Tele")
_updateTelemetry.start()
time.sleep(4)
_updateTelemetry.stop()
time.sleep(2)
_updateTelemetry.resume()
print 'herhe'
while True:
	print common_vars.vianSLat
	common_vars.vianSLat +=1000
	print math.sin(90)
	time.sleep(1)
	pass


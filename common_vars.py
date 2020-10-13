#https://mavlink.io/en/messages/common.html#MISSION_ITEM_INT
#https://mavlink.io/en/messages/common.html#MAV_CMD

from common_import import *
import numpy as np
import threading
import time
import establish_link
from pymavlink.dialects.v20 import ardupilotmega as mavlink2

vianSGNSS = [0.00, 0.00, 0.00] # Lat Lon Alt
vianSAltitude = [0.00, 0.00, 0.00] # R  P Y
# RC0 (ignore this) RC1, RC2, RC3, RC4, RC5, RC6, RC7, RC8, RC9, RC10, RC11 
vianSRCSBUS = [1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100, 1100]

vianSCurrenMode = 0
vianSMissionList = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0]]) 

vianSCurrentMission = 0
linkAP = 0
vianCurrentMode = 0
vianPreviousMode = 0
vianWaypoint = []
# This class updates:
# . GNSS - vianSGNSS
# . Ground Speed

def latLongReturnAngle(latA, longA, latB, longB):
	temp = math.atan2(longB - longA, latB - latA) * (180.00 / math.pi)
	if temp <=0:
		temp = 360 + temp
	return temp
    
class updateTelemetry(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.running = True   
		self._term = False 
	def run(self):
		global vianSGNSS
		while True and not self._term:
			if self.running:
				if linkAP != 0:
					msg = linkAP.recv_match()
					if not msg:
						continue
					if msg.get_type() == 'GLOBAL_POSITION_INT':
						vianSGNSS[0] = float(msg.lat)/ 1e7
						vianSGNSS[1] = float(msg.lon)/ 1e7
						vianSGNSS[2] = float(msg.alt)/ 1e3
					
						continue
					if msg.get_type() == 'RC_CHANNELS':
						vianSRCSBUS[1] = msg.chan1_raw
						vianSRCSBUS[2] = msg.chan2_raw
						vianSRCSBUS[3] = msg.chan3_raw
						vianSRCSBUS[4] = msg.chan4_raw
						vianSRCSBUS[5] = msg.chan5_raw
						vianSRCSBUS[6] = msg.chan6_raw
						vianSRCSBUS[7] = msg.chan7_raw
						vianSRCSBUS[8] = msg.chan8_raw
						vianSRCSBUS[9] = msg.chan9_raw
						vianSRCSBUS[10] = msg.chan10_raw
						vianSRCSBUS[11] = msg.chan11_raw
						continue
					if msg.get_type() == 'MISSION_CURRENT':
						vianSCurrentMission = msg.seq
						continue
					if msg.get_type() == 'HEARTBEAT':
							#https://ardupilot.org/dev/docs/apmcopter-adding-a-new-flight-mode.html
							#17 is break
						if msg.custom_mode == 0: 
							vianSCurrenMode = 'STAB'
							continue
						if msg.custom_mode == 2: 
							vianSCurrenMode = 'ALTH'
							continue
						if msg.custom_mode == 3: 
							vianSCurrenMode = 'AUTO'
							continue
						if msg.custom_mode == 5: 
							vianSCurrenMode = 'LOIT'
							continue
						if msg.custom_mode == 6: 
							vianSCurrenMode = 'RTL'
							continue
						continue
						
					
			
	def pause(self):
		#self._stop_event.set()
		self.running = False
	def resume(self):
		self.running = True
	def stop(self):
		self._term = True

class updateWaypoint(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.running = True   
		self._term = False 
		self.done = False
	def run(self):
		global vianSMissionList
		while not self._term:
			
			if self.running and not self.done:
				
				vianSMissionList = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0]]) 
				mss = mavlink2.MAVLink_mission_request_list_message(
												linkAP.target_system,
												linkAP.target_component,
												0)
				linkAP.mav.send(mss)
				itera = 0
				#print '----------------------------------------------'
				while True and not self.done:
					msg = linkAP.recv_match() # catching until "MISSION_COUNT" appears
					if not msg:
						continue
					if msg.get_type() == 'MISSION_COUNT':
						#print msg
						itera = int(msg.count)
						if itera == 0:
							print 'No missions'
							self.done = True
							break
							
						else:
							for i in range(itera):
								mss = mavlink2.MAVLink_mission_request_int_message(
									linkAP.target_system,
									linkAP.target_component,
									i,
									0)
								linkAP.mav.send(mss)
								while True:
									msg = linkAP.recv_match()
									if not msg:
										continue
									if msg.get_type() == 'MISSION_ITEM_INT': # catching until "MISSION_ITEM_INT" appears
										#print msg
										if i != 0:
											vianSMissionList = np.append(vianSMissionList, 
															[[0,0,0,0,0,0,0,0,0,0,0,0,0,0]], axis = 0)
										
										vianSMissionList[i,0] = int(msg.target_system)
										vianSMissionList[i,1] = int(msg.target_component)
										vianSMissionList[i,2] = int(msg.seq)
										vianSMissionList[i,3] = int(msg.frame)
										vianSMissionList[i,4] = int(msg.command)
										vianSMissionList[i,5] = int(msg.current)
										vianSMissionList[i,6] = int(msg.autocontinue)
										vianSMissionList[i,7] = float(msg.param1)
										vianSMissionList[i,8] = float(msg.param2)
										vianSMissionList[i,9] = float(msg.param3)
										vianSMissionList[i,10] = float(msg.param4)
										vianSMissionList[i,11] = int(msg.x)
										vianSMissionList[i,12] = int(msg.y)
										vianSMissionList[i,13] = float(msg.z)												
										break
								if i == itera -1:
									
									print 'Done reading mission list'
									self.done = True
									break
					
			
	def pause(self):
		#self._stop_event.set()
		self.running = False
	def resume(self):
		self.running = True
	def stop(self):
		self._term = True


def angleToNextWP():
	if vianSMissionList[vianSCurrentMission,4] == 16:
		return latLongReturnAngle(vianSGNSS[0], 
		vianSGNSS[1], 
		float(vianSMissionList[vianSCurrentMission,11]) / 7 , 
		float(vianSMissionList[vianSCurrentMission,12]) / 7)
		

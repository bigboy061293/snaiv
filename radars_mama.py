from common_import import *
import can
import threading
import numpy as np
import queue
import cmd_msg
import common_vars
que = queue.Queue()
#border +-45 degree for OA https://ardupilot.org/dev/docs/code-overview-object-avoidance.html
bordersEightSectors = [67.5, 22.5, 337.5, 292.5, 247.5, 202.5, 157.5, 112.5]
degreeEachSectors = 45.00

vianSCanBus = can.Bus(channel = 'can0', interface = 'socketcan', bitrate=500000)
radarMaxRangeMet = 40
radarMinRangeMet = 0.1
radarMaxRange = 4001
radarMinRange = 30
sectorEight = [radarMaxRange,radarMaxRange,radarMaxRange,radarMaxRange,
			radarMaxRange,radarMaxRange,radarMaxRange,radarMaxRange]
sectorMulti = [[0.0,0.0]]
timeOut = [0,0,0,0,0]
timeCount = [0,0,0,0,0]
timeOutSet = 100
radarTick = 0
radarTickSet = 10
readarReadyToRead = 0
mr72appear=[0,0,0,0]
mr72ThreeSectors=[radarMaxRange,radarMaxRange,radarMaxRange,
				radarMaxRange,radarMaxRange,radarMaxRange,
				radarMaxRange,radarMaxRange,radarMaxRange,
				radarMaxRange,radarMaxRange,radarMaxRange]
nra24 = 0
nra24appear = 0
def xyReturnSec(x,y, degreeDec):
	abc = math.atan2(y,x) * (180.00 / math.pi)
	abc = int(abc * 100)
	while not abc % (degreeDec*100) == 0:
		
		abc = abc + 1
		#print abc
	seccc = round(abc / (degreeDec*100))
	mag = math.sqrt(pow(x,2) + pow(y,2))
	return seccc, mag

def inTheSectors(deg, bordersEightSectors):
	if (deg >= 0 and deg < bordersEightSectors[1]):
		deg += 360
	if (deg >= bordersEightSectors[0]) and (deg < bordersEightSectors[7]):
		return 0
	if (deg >= bordersEightSectors[1]) and (deg < bordersEightSectors[0]):
		return 1
	if (deg >= bordersEightSectors[2]) and (deg <= bordersEightSectors[1] + 360):
		return 2
	if (deg >= bordersEightSectors[3]) and (deg < bordersEightSectors[2]):
		return 3
	if (deg >= bordersEightSectors[4]) and (deg < bordersEightSectors[3]):
		return 4
	if (deg >= bordersEightSectors[5]) and (deg < bordersEightSectors[4]):
		return 5
	if (deg >= bordersEightSectors[6]) and (deg < bordersEightSectors[5]):
		return 6
	if (deg >= bordersEightSectors[7]) and (deg < bordersEightSectors[6]):
		return 7
	#return 'None'
	
class updateProcess(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.running = True   
		self._term = False 
	def run(self):
		global sectorEight
		global sectorMulti
		np.set_printoptions(precision=3)
		np.set_printoptions(suppress=True)
		while True:
			
			#print mr72ThreeSectors
			#mr72ThreeSectors
			#print timeOut
			cmd_msg.sendMessageDistanceSensor(common_vars.linkAP,min (int(mr72ThreeSectors[0]*100),
																	int(mr72ThreeSectors[11]*100))
																		,7)
																		
																		
			cmd_msg.sendMessageDistanceSensor(common_vars.linkAP,int(mr72ThreeSectors[1]*100),0)
			
			cmd_msg.sendMessageDistanceSensor(common_vars.linkAP,min (int(mr72ThreeSectors[2]*100),
																	int(mr72ThreeSectors[3]*100))
																		,1)
																		
			cmd_msg.sendMessageDistanceSensor(common_vars.linkAP,int(mr72ThreeSectors[4]*100),2)
			
			cmd_msg.sendMessageDistanceSensor(common_vars.linkAP,min (int(mr72ThreeSectors[5]*100),
																	int(mr72ThreeSectors[6]*100))
																		,3)
			
			cmd_msg.sendMessageDistanceSensor(common_vars.linkAP,int(mr72ThreeSectors[7]*100),4)
			
			cmd_msg.sendMessageDistanceSensor(common_vars.linkAP,min (int(mr72ThreeSectors[8]*100),
																	int(mr72ThreeSectors[9]*100))
																		,5)
			
			cmd_msg.sendMessageDistanceSensor(common_vars.linkAP,int(mr72ThreeSectors[10]*100),6)
																		
																		
																		
			
			"""
			if not readarReadyToRead:
					continue
			
			while (que.empty() == False):
				#print que.qsize()
				secinQ = que.get()
				if secinQ[1] < radarMinRangeMet:
					continue
				tempIn = inTheSectors(secinQ[0], bordersEightSectors)
				temp[tempIn] = round(float(min(secinQ[1],temp[tempIn])), 2)
			print temp
			
			
			for point in secinQ:
				if point[1] < radarMinRangeMet:
					continue
				tempIn = inTheSectors(point[0], bordersEightSectors)
				#print point, inTheSectors(point[0], bordersEightSectors)
				
				temp[tempIn] = round (float (min(point[1], temp[tempIn])), 2)
			print sectorMulti
			print temp
			#print timeOut
			"""
			#sectorMulti = [[0,0]]
	def pause(self):
		self.running = False
	def resume(self):
		self.running = True
	def stop(self):
		self._term = True
def constraintNew(num, up, down):
	a = num
	if a >= up:
		a = up
	if a <= down:
		a = down
	return a
class readRadarThree(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.running = True   
		self._term = False 
		self.mr72appear = [0,0,0,0]
	def run(self):
		global sectorMulti
		global timeCount
		global timeOut
		global readarReadyToRead
		global mr72appear
		global mr72ThreeSectors
		while True and not self._term:
			if self.running:
			
				
				
				
				canMessage = vianSCanBus.recv(1.0)  #need to process this!!!
				# this bug:
				# if no radars connect at the first time
				# this will hang
				# and the entire program will not run
				# !!! wtf
				if canMessage == None:
					continue
				#if canMessage is None:
				#	print 'ngu'
				#canMessage = vianSCanBus._recv_internal()
				#print canMessage
				
				if canMessage.arbitration_id == 0X60B: #front
					y = (canMessage.data[1] * 32 + (canMessage.data[2] >> 3)) * 0.2 - 500
					x = ((canMessage.data[2]&0X07) * 256 + canMessage.data[3]) * 0.2 - 204.6
					sector, mag = xyReturnSec(x,y,1)
					mag = round(mag,2)
					rg = (canMessage.data[6] >> 3) & 0X03	
					"""
					if (sector, mag) not in sectorMulti:
						sectorMulti = np.append(sectorMulti,[[sector,mag]],axis = 0)
					cfr +=1
					cfr = constraintNew(cfr,0,3)
					"""
					if rg == 1:
						mr72ThreeSectors[0] = mag
					elif rg ==2 :
						mr72ThreeSectors[1] = mag
					elif rg == 3:
						mr72ThreeSectors[2] = mag
						
					
				elif canMessage.arbitration_id == 0X61B: #right
					y = (canMessage.data[1] * 32 + (canMessage.data[2] >> 3)) * 0.2 - 500
					x = ((canMessage.data[2]&0X07) * 256 + canMessage.data[3]) * 0.2 - 204.6
					sector, mag = xyReturnSec(x,y,1)
					mag = round(mag,2)
					"""
					sector+=270
					if sector > 360:
						sector-=360
					if (sector, mag) not in sectorMulti:
						sectorMulti = np.append(sectorMulti,[[sector,mag]],axis = 0)
					cri +=1
					cri = constraintNew(cri,0,3)
					"""
					rg = (canMessage.data[6] >> 3) & 0X03	
				
					if rg == 1:
						mr72ThreeSectors[3] = mag
					elif rg ==2 :
						mr72ThreeSectors[4] = mag
					elif rg == 3:
						mr72ThreeSectors[5] = mag
					
				elif canMessage.arbitration_id == 0X62B: #rear
					y = (canMessage.data[1] * 32 + (canMessage.data[2] >> 3)) * 0.2 - 500
					x = ((canMessage.data[2]&0X07) * 256 + canMessage.data[3]) * 0.2 - 204.6
					sector, mag = xyReturnSec(x,y,1)
					mag = round(mag,2)
					"""
					sector+=180
					if sector > 360:
						sector-=360
					if (sector, mag) not in sectorMulti:
						sectorMulti = np.append(sectorMulti,[[sector,mag]],axis = 0)
					cre+=1
					cre = constraintNew(cre,0,3)
					"""
					rg = (canMessage.data[6] >> 3) & 0X03	
				
					if rg == 1:
						mr72ThreeSectors[6] = mag
					elif rg ==2 :
						mr72ThreeSectors[7] = mag
					elif rg == 3:
						mr72ThreeSectors[8] = mag

				elif canMessage.arbitration_id == 0X63B: #left
					y = (canMessage.data[1] * 32 + (canMessage.data[2] >> 3)) * 0.2 - 500
					x = ((canMessage.data[2]&0X07) * 256 + canMessage.data[3]) * 0.2 - 204.6
					sector, mag = xyReturnSec(x,y,1)
					mag = round(mag,2)
					"""
					sector+=90
					
					if (sector, mag) not in sectorMulti:
						sectorMulti = np.append(sectorMulti,[[sector,mag]],axis = 0)
					cle+=1
					cle = constraintNew(cle,0,3)\
					"""
					rg = (canMessage.data[6] >> 3) & 0X03	
					if rg == 1:
						mr72ThreeSectors[9] = mag
					elif rg ==2 :
						mr72ThreeSectors[10] = mag
					elif rg == 3:
						mr72ThreeSectors[11] = mag
				elif canMessage.arbitration_id == 0X70C:
					nra24 = canMessage.data[2]*256 + canMessage.data[3]
					print nra24
				elif canMessage.arbitration_id == 0X60A: #cycle check mr72_0, front
					timeCount[0] = 0
					mr72appear[0] = 1
				elif canMessage.arbitration_id == 0X61A: #cycle check mr72_1, right
					timeCount[1] = 0
					mr72appear[1] = 1
				elif canMessage.arbitration_id == 0X62A: #cycle check mr72_2, rear
					timeCount[2] = 0
					mr72appear[2] = 1
				elif canMessage.arbitration_id == 0X63A: #cycle check mr72_3, left
					timeCount[3] = 0
					mr72appear[3] = 1
				elif canMessage.arbitration_id == 0X65A: #cycle check nra24
					timeCount[4] = 0
					nra24appear = 1
				
				
	def pause(self):
		#self._stop_event.set()
		self.running = False
	def resume(self):
		self.running = True
	def stop(self):
		self._term = True

class radarCounter(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.running = True   
		self._term = False 
		global sectorEight
	def run(self):
			while True:
				
				timeCount[0] += 1
				timeCount[1] += 1
				timeCount[2] += 1
				timeCount[3] += 1
				timeCount[4] += 1
				for i in range(5):
					if timeCount[i] > timeOutSet:
						timeOut[i] = 1
					else:
						timeOut[i] = 0
					
					
				#print timeOut
				time.sleep(0.01)
	def pause(self):
		self.running = False
	def resume(self):
		self.running = True
	def stop(self):
		self._term = True

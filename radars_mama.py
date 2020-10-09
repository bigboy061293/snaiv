from common_import import *
import can
import threading
import numpy as np
vianSCanBus = can.interface.Bus('can0', bustype = 'socketcan_native')
radarMaxRangeMet = 40
radarMinRangeMet = 0.1
radarMaxRange = 4001
sectorEight = [radarMaxRange,radarMaxRange,radarMaxRange,radarMaxRange,
			radarMaxRange,radarMaxRange,radarMaxRange,radarMaxRange]
sectorMulti = [[0.0,0.0]]
def xyReturnSec(x,y, degreeDec):
	abc = math.atan2(y,x) * (180.00 / math.pi)
	abc = int(abc * 100)
	while not abc % (degreeDec*100) == 0:
		
		abc = abc + 1
		#print abc
	seccc = round(abc / (degreeDec*100))
	mag = math.sqrt(pow(x,2) + pow(y,2))
	return seccc, mag
	
	
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
		while True:
			time.sleep(0.01)
			#sectorEight[0] = sectorMulti
			if np.size(sectorMulti,0) > 2:
				#print np.size(sectorMulti,1)
				#print sectorMulti
				if np.size(sectorMulti,0) == 1:
					continue
				else:
					sector0 = (sectorMulti[:,0] > 67.5) & (sectorMulti[:,0] < 112.5)
				newSec = sectorMulti[sector0]
				print newSec
			#print sectorMulti
			#print sector0
			sectorMulti = [[0,0]]
	def pause(self):
		self.running = False
	def resume(self):
		self.running = True
	def stop(self):
		self._term = True
class readRadarThree(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.running = True   
		self._term = False 
	def run(self):
		global sectorMulti
		while True and not self._term:
			if self.running:
				canMessage = vianSCanBus.recv() 
				if canMessage.arbitration_id == 0X60B: #front
					y = (canMessage.data[1] * 32 + (canMessage.data[2] >> 3)) * 0.2 - 500
					x = ((canMessage.data[2]&0X07) * 256 + canMessage.data[3]) * 0.2 - 204.6
					sector, mag = xyReturnSec(x,y,1)
					sectorMulti = np.append(sectorMulti,[[sector,mag]],axis = 0)
					
					
				elif canMessage.arbitration_id == 0X61B: #right
					y = (canMessage.data[1] * 32 + (canMessage.data[2] >> 3)) * 0.2 - 500
					x = ((canMessage.data[2]&0X07) * 256 + canMessage.data[3]) * 0.2 - 204.6
					sector, mag = xyReturnSec(x,y,1)
					sector+=270
					if sector > 360:
						sector-=360
					sectorMulti = np.append(sectorMulti,[sector,mag])
					
					
				elif canMessage.arbitration_id == 0X62B: #rear
					y = (canMessage.data[1] * 32 + (canMessage.data[2] >> 3)) * 0.2 - 500
					x = ((canMessage.data[2]&0X07) * 256 + canMessage.data[3]) * 0.2 - 204.6
					sector, mag = xyReturnSec(x,y,1)
					sector+=180
					if sector > 360:
						sector-=360
					sectorMulti = np.append(sectorMulti,[sector,mag])
					

				elif canMessage.arbitration_id == 0X63B: #left
					y = (canMessage.data[1] * 32 + (canMessage.data[2] >> 3)) * 0.2 - 500
					x = ((canMessage.data[2]&0X07) * 256 + canMessage.data[3]) * 0.2 - 204.6
					sector, mag = xyReturnSec(x,y,1)
					sector+=90
					
					sectorMulti = np.append(sectorMulti,[sector,mag])
		
	def pause(self):
		#self._stop_event.set()
		self.running = False
	def resume(self):
		self.running = True
	def stop(self):
		self._term = True

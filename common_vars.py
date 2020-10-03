import threading
import time

vianSLat = 0
vianSLong = 0
vianSAlt = 0
linkAP = 0
vianCurrentMode = 0
vianPreviousMode = 0
vianWaypoint = []
class updateTelemetry(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.running = True   
		self._term = False 
	def run(self):
		global vianSLat
		while True and self._term:
			if self.running:
				if linkAP != 0:
					msg = linkAP.recv_match()
					if not msg:
						continue
					print msg
			
	def pause(self):
		#self._stop_event.set()
		self.running = False
	def resume(self):
		self.running = True
	def stop(self)
		self._term = True

class updateWaypoint(threading.Thread):
		def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.running = True    
	def run(self):
		global vianSLat
		while True and self._term:
			if self.running:
				if linkAP != 0:
					msg = linkAP.recv_match()
					if not msg:
						continue
					print msg
			
	def pause(self):
		#self._stop_event.set()
		self.running = False
	def resume(self):
		self.running = True
	def stop(self)
		self._term = True

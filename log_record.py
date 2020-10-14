from common_import import *
import threading
import psutil
import time

from datetime import datetime

#import radars_mama
#import common_vars
#import

DO_LOG_FILE = True
if DO_LOG_FILE:
	logFileNow  = datetime.now()
	fileNow = open('log/' + str(logFileNow) + '.txt', 'w')
	fileNow.close()
class logging(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.running = True   
		self._term = False 
	def run(self):
		
		while True and not self._term:
			if self.running:
				time.sleep(0.1)
				
				
				if DO_LOG_FILE:
					fileNow = open('log/' + str(logFileNow) + '.txt', 'a')
					logString = (str(datetime.now())
								+ str(input_output.pumpFail)
								+ str(radars_mama.timeOut)
									+'\n')
					#print logString
					fileNow.write(logString)
					fileNow.close()
				#print psutil.cpu_temperature()
				#print psutil.sensors_temperatures()
			
					
			
	def pause(self):
		#self._stop_event.set()
		self.running = False
	def resume(self):
		self.running = True
	def stop(self):
		self._term = True

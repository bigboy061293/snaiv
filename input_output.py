from common_import import *
import threading
import os
import subprocess, signal
#import Jetson.GPIO as GPIO
import RPi.GPIO as GPIO
import time
from datetime import datetime
import numpy as np
keyIp = ''

flowPin = 36
timebefore = 0
timenow = 0
pulse = 0
now = datetime.now()
#set_point_fr = 1
pumpQ = 0
pumpFlowRateSetpoint = 1

#k = 5
pumpFilterK = 5
pumpLevelFilterK = 20
#smith = 0.15
pumpSmith = 0.15
#kern=np.ones(2*k+1)/(2*k+1)
#pumpKern=np.ones(2*k+1)/(2*k+1)
#fr_value_raw = np.zeros(2*k + 1)
pumpFlowRateRaw = np.zeros(2*pumpFilterK + 1)
pumpLevelRaw = np.zeros((2*pumpLevelFilterK + 1,2))
#pump_servo = 1100
pumpServo = 1100
pumpServoMin = 1050
pumpServoMax = 1950

GPIO_PUMP = 36 #36 in header pin 1 to 40
GPIO_LOWER_LEVEL_SENSOR = 32
GPIO_UPPER_LEVEL_SENSOR = 31

pumpLowerLevel = 0
pumpUpperLevel = 0
pumpLevelFiltered = [0 ,0]
pumpFail = False
pumpFailSetTime = 100000
pumpFailCountStep = 1
pumpFailCounter = 0
#pumpFailTimeNow = get_time_now_in_us()
#pumpFailTimeBefore = 0
def get_time_now_in_us():
	now = datetime.utcnow()
	(dt, micro) = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f').split('.')
	micro = (long(dt[8:10]) * 3600 * 1000000 +
				 long(dt[10:12])* 60 * 1000000 +
				 long(dt[12:14]) * 1000000) + long(micro)
	return micro
timenow = get_time_now_in_us()
timebefore = get_time_now_in_us()
def constraintNew(num, up, down):
	a = num
	if a >= up:
		a = up
	if a <= down:
		a = down
	return a
def calculateQ(self):
	global pumpQ
	global timenow
	global timebefore
	timenow = get_time_now_in_us()
	f =  1/(float(timenow - timebefore)) * 1000000
	pumpQ = (f+3)/23
	timebefore = get_time_now_in_us()
def calcUperLevel(self):
	global pumpUpperLevel
	if GPIO.input(GPIO_UPPER_LEVEL_SENSOR) == 1:
		pumpUpperLevel = 1
	elif GPIO.input(GPIO_UPPER_LEVEL_SENSOR) == 0:
		pumpUpperLevel = 0

def calcLowerLevel(self):
	global pumpUpperLevel
	if GPIO.input(GPIO_LOWER_LEVEL_SENSOR) == 1:
		pumpLowerLevel = 1
	elif GPIO.input(GPIO_LOWER_LEVEL_SENSOR) == 0:
		pumpLowerLevel = 0
def initializeJNIO():    
	GPIO.setmode(GPIO.BOARD)
	#set pump input
	GPIO.setup(GPIO_PUMP,GPIO.IN)
	
	GPIO.add_event_detect(GPIO_PUMP, GPIO.RISING, callback = calculateQ, bouncetime = 1)
	GPIO.setup(GPIO_UPPER_LEVEL_SENSOR,GPIO.IN)
	GPIO.add_event_detect(GPIO_UPPER_LEVEL_SENSOR, GPIO.BOTH, callback = calcUperLevel, bouncetime = 1)
	#GPIO.add_event_detect(GPIO_UPPER_LEVEL_SENSOR, GPIO.FALLING, callback = calcUperLevel, bouncetime = 1)
	GPIO.setup(GPIO_LOWER_LEVEL_SENSOR,GPIO.IN)
	GPIO.add_event_detect(GPIO_LOWER_LEVEL_SENSOR, GPIO.BOTH, callback = calcLowerLevel, bouncetime = 1)
	#GPIO.add_event_detect(GPIO_LOWER_LEVEL_SENSOR, GPIO.FALLING, callback = calcLowerLevel, bouncetime = 1)
def pumpResume():
	global pumpFail
	pumpFail = False
class pumpControl(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.running = True   
		self._term = False 
	def run(self):
		global pumpFlowRateSensor
		global pumpFlowRateRaw
		global pumpFlowRateFiltered
		global pumpServo
		
		global pumpLevelRaw
		global pumpLevelSensor
		global pumpLevelFiltered
		global pumpFail
		global pumpFailCounter
		while True and not self._term:
			if self.running:
				pumpFlowRateSensor = pumpQ ## read fr from sensor
				pumpFlowRateRaw = np.roll(pumpFlowRateRaw,-1) # rolling in the deep
				pumpFlowRateRaw[2*pumpFilterK] = pumpFlowRateSensor 
				pumpFlowRateFiltered = np.average(pumpFlowRateRaw)
				
				
				if pumpFlowRateFiltered < (pumpFlowRateSetpoint - pumpSmith):
					pumpServo+=5
				elif pumpFlowRateFiltered > (pumpFlowRateSetpoint + pumpSmith):
					pumpServo-=5
				pumpServo = constraintNew(pumpServo,pumpServoMin,pumpServoMax)
				
				# need calib this shiettttt
				if pumpFail == False:
				
					if (pumpFlowRateFiltered > (pumpFlowRateSetpoint - pumpSmith) and
						pumpFlowRateFiltered < (pumpFlowRateSetpoint + pumpSmith)):
							pumpFailCounter = 0
					else:
						pumpFailCounter+=pumpFailCountStep
					if pumpFailCounter > pumpFailSetTime:
						pumpFail = True
						pumpFailCounter = 0
				
				pumpLevelSensor = [pumpLowerLevel, pumpUpperLevel]
				pumpLevelRaw = np.roll(pumpLevelRaw,-1, axis = 0) # rolling in the deep
				
				pumpLevelRaw[2*pumpLevelFilterK] = pumpLevelSensor
				pumpLevelFiltered = np.average(pumpLevelRaw,axis = 0)
				
				#print pumpLevelFiltered
				#print pumpFail
				# pumpLevelFiltered[0] is lower: 0..1
				# pumpLevelFiltered[1] is upper: 0..1
				
				# check pump fail if Q <> Q set in certain of time
				# check level meter > or < threshol -> con nuoc trong binh
				if not pumpFail and pumpLevelFiltered[0] > 0.7 and pumpLevelFiltered[1] > 0.7:
					cmd_msg.sendMessageDistanceSensor_RC9(common_vars.linkAP,pumpServo)
				else:
					cmd_msg.sendMessageDistanceSensor_RC9(common_vars.linkAP,pumpServoMin)
					
			time.sleep(0.01)
	
	def pause(self):
		#self._stop_event.set()
		self.running = False
	def resume(self):
		self.running = True
	def stop(self):
		self._term = True
class keyboardInput(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.running = True  
		self.command = '' 
	
	def run(self):
		global keyIp
		try:
			while True:
				command = raw_input()
				if command == 'a':
					pass 
				elif command == 'load mission':
					keyIp = command
				elif command[0:8]  == 'wpspeed,':
					keyIp = command
				elif command[0] == 't':
					
					
					print ('Terminating process: ', os.getpid())
					os.kill(os.getpid(), signal.SIGKILL)
				else:
					print '------------ No commands found! ------------'
		except Exception: 
			print('Except from Input')

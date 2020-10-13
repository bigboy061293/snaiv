import Jetson.GPIO as GPIO
import time
from datetime import datetime
from pymavlink import mavutil
import threading
import subprocess, signal
from pymavlink.dialects.v20 import ardupilotmega as mavlink2
import os
import numpy as np
import math

lph = 20
drone_speed = 3
nozzle_angle = 2
drone_alt = 2
adjust_coeff = 60
covered_area = math.pi* (drone_alt * math.tan(nozzle_angle/2))**2
lpm = adjust_coeff*(lph * drone_speed * 60)/ (covered_area*10000)
#print lpm
#while True:
#	pass

WRITE_FILE = 0
flowPin = 36
timebefore = 0
timenow = 0
pulse = 0
now = datetime.now()
set_point_fr = 1
Q = 0
k = 5
smith = 0.15
kern=np.ones(2*k+1)/(2*k+1)
fr_value_raw = np.zeros(2*k + 1)
pump_servo = 1100


if WRITE_FILE:
	print ('Input file name: ')
	fileName = raw_input()
	pulse = int(fileName)
	fileName = 'logBom/' + fileName + '.txt'
	fileLog = open(fileName, 'w')


def outRC9(pulse):
	UINT16_MAX = 65535
	mss = mavlink2.MAVLink_rc_channels_override_message(
					0,
					0,
					UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, 
					pulse, 
					UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX, UINT16_MAX)
	master.mav.send(mss)

class readInputThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		
	def run(self):
		global pulse
		global set_point_fr
		while True:
		 
			command = raw_input()
			if command == 'echo':
				print ('.^^.')
				continue
				   
				
			elif command == 't':
				if WRITE_FILE:
					fileLog.close()
				print ('Terminating process: ', os.getpid())
				os.kill(os.getpid(), signal.SIGKILL)
				continue
			else: 
				
				set_point_fr = float(command)
				
				continue

def get_time_now_in_us():
	now = datetime.utcnow()
	(dt, micro) = datetime.utcnow().strftime('%Y%m%d%H%M%S.%f').split('.')
	micro = (long(dt[8:10]) * 3600 * 1000000 +
				 long(dt[10:12])* 60 * 1000000 +
				 long(dt[12:14]) * 1000000) + long(micro)
	return micro
timenow = get_time_now_in_us()
timebefore = get_time_now_in_us()
def printDump(self):
	global Q
	global timenow
	global timebefore
	timenow = get_time_now_in_us()
	f =  1/(float(timenow - timebefore)) * 1000000
	Q = (f+3)/23
	#print Q
	
	timebefore = get_time_now_in_us()
	

GPIO.setmode(GPIO.BOARD)
GPIO.setup(36,GPIO.IN)


GPIO.add_event_detect(36, GPIO.RISING, callback = printDump, bouncetime = 0)

master = mavutil.mavlink_connection('tcp:192.168.0.210:20002', dialect = "ardupilotmega")

_threadReadInput = readInputThread(1, "Read input")
_threadReadInput.start()

try:
	while True:
		time.sleep(0.05)
		
		fr_sensor = Q # read fr from sensor
		fr_value_raw = np.roll(fr_value_raw,-1) # rolling in the deep
		fr_value_raw[2*k] = fr_sensor 
		
		#out=np.convolve(fr_value_raw,kern, mode='same')
		out = np.average(fr_value_raw)
		#fr_filtered = out[2*k]
		fr_filtered = out
		#print 'Set LPM: ', set_point_fr, ', ',Q,', ', fr_filtered,', ', pump_servo
		print 'Set LPM: ', set_point_fr, ', ', ' Current LPM: ', fr_filtered,', ', 'Current PWM: ', pump_servo
		if fr_filtered < (set_point_fr - smith):
			pump_servo+=5
		#output 
		elif fr_filtered > (set_point_fr + smith):
			pump_servo-=5
		if pump_servo < 1100:
			pump_servo = 1100
		elif pump_servo >1900:
			pump_servo = 1900
		
		
		outRC9(pump_servo)
		if WRITE_FILE:
			fileLog.write(str(Q))
			fileLog.write(',')
			fileLog.write(str(fr_filtered))
			fileLog.write(',')
			fileLog.write(str(pulse))
			fileLog.write(',')
			fileLog.write(str(set_point_fr))
			fileLog.write('\n')
		

finally:
	GPIO.cleanup()


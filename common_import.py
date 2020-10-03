try:
	from pymavlink import mavutil
except:
	print "No PyMAVutil"
	
import time

import math

import common_vars
SIMULATOR_UDP = 'udp:127.0.0.1:14550'
TCP_650 = 'tcp:192.168.0.210:20002'
SIMULATOR_TCP = 'tcp:127.0.0.1:5762'
VIANS_DATALINK_MODULE = 'tcp:192.168.0.210:20002'
COMPANION_PC_SERIAL = '/dev/ttyS0'
COMPANION_PC_BAUD = 115200

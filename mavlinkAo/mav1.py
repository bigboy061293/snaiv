from pymavlink import mavutil
#from pymavlink.dialects.v10 import ardupilotmega as mavlink1
#from pymavlink.dialects.v20 import ardupilotmega as mavlink2
import socket
import time
import math
import inspect
import threading
import os
import ctypes

import subprocess, signal
import numpy as np
from datetime import datetime

THIS_F_JN = 'tcp:127.0.0.1:2993'

master = mavutil.mavlink_connection(THIS_F_JN, dialect = "ardupilotmega", source_system = 29, source_component = 29)
print 'Done Mav Con'
def pinging(master):
    msg = None
    while not msg:
        master.mav.ping_send(
            time.time(), # Unix time
            0, # Ping number
            0, # Request ping of all systems
            0 # Request pping of all components
        )
        msg = master.recv_match()
        #print msg
        #time.sleep(0.5)
HOST = '127.0.0.1'
PORT = 2993	
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((HOST, PORT))
master.target_system = 29
master.target_component = 30

while True:

	#s.sendall(b'asdasd')
	#master.mav.ping_send(
    #        time.time(), # Unix time
    #        0, # Ping number
    #        0, # Request ping of all systems
    #        0 # Request pping of all components
    #    )
	#data = s.recv(1024)
	#print (repr(data))
	#pinging(master)
	master.mav.command_long_send(
		master.target_system, master.target_component,
		mavutil.mavlink.MAV_CMD_USER_1,
		0,
		1,2,3,4,5,6,7)
	time.sleep(0.5)
	print master.target_system
	print master.target_component
	time.sleep(1)

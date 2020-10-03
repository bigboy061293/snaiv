#from pymavlink import mavutil
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

THIS_F_JN = 'tcp:127.0.0.1:2992'

#master = mavutil.mavlink_connection(THIS_F_JN, dialect = "ardupilotmega")
modname = 'pymavlink.dialects.v10.ardupilotmega'
mod = __import__(modname)
components = modname.split('.')
print components
for comp in components[1:]:
	mod = getattr(mod,comp)

print mod
mavlink = mod
mav = mavlink.MAVLink(29, 30,True)
mav.srcSystem = 29
mav.srcComponent = 30


HOST = '127.0.0.1'
PORT = 2993
s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn,addr = s.accept()
print ('coned by', addr)
while True:
	data = conn.recv(1024)
	#msg = 
	print data
	print mav.parse_char(data)
	time.sleep(0.5)
	#conn.sendall(data)
"""
while True:
	msg = master.recv_match()
	if not msg:
		continue
	print msg
"""

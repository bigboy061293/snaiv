from common_import import *
import threading
import os
import subprocess, signal
keyIp = ''
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
		if command == 'load mission':
		    keyIp = command
		elif command[0:8]  == 'wpspeed,':
		    keyIp = command
                elif command == 't':
                    #fileNow.close()
                    print ('Terminating process: ', os.getpid())
                   
                    os.kill(os.getpid(), signal.SIGKILL)
		
        except Exception: 
            print('Except from Input')

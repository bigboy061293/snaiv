from common_import import *

command =''

class keyboardInput:
    def __init__(self):
	threading.Thread.__init__(self)
	self.threadID = threadID
	self.name = name
	self.running = True    
    def run(self):
	try:
	    while True:
                command = raw_input()
                if command == 'a':
		    pass
                elif command == 't':
                    #fileNow.close()
                    print ('Terminating process: ', os.getpid())
                   
                    os.kill(os.getpid(), signal.SIGKILL)
         
        except Exception: 
            print('Except from Input')

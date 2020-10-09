from common_import import *


def connectVianS(master):
    msg = None
    while not msg:
        master.mav.ping_send(
            time.time(), # Unix time
            0, # Ping number
            1, # Request ping of all systems
            1 # Request pping of all components
        )
        msg = master.recv_match()
        print msg
        time.sleep(0.5)
        




class sensors_collectors:
	def __init__(self):
		pass
	def update(self):
		pass

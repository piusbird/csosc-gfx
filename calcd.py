## Module: calcd.py
## dumb calulator server


from socket import *
from calcsrv.config import *
from calcsrv.ProtocalHandler import ProtocalHandler
from calcsrv.misc import NullDevice
import os
import sys
 

print "Calcd 0.0.1 Starting...\n"
srvsock = socket(AF_INET, SOCK_STREAM)
srvsock.bind((INET_ADDR, PORT))
srvsock.listen(MAX_CONNS)
print "Server Bound\n"
print "Opening log file\n"
fp = open("calcd.log", "a")
print "Forking..."

pid = os.fork() ## Hmmm this looks an awful lot like... C

if pid:
	os._exit(0) # kill the parent
else:
	## directions say this will stop exceptions while
	## deamonized. Which would be bad
	os.setpgrp()
	os.umask(0)
	
	print os.getpid() # to aid in stoping the server
	# Run silent, run deep
	sys.stdin.close() 
	sys.stdout = NullDevice()
	sys.stderr = NullDevice()
		
while True:
	chann, det = srvsock.accept()
	fp.write(str(det) + " Connected Starting ProtocalHandler\n")
	fp.flush()
	ProtocalHandler(chann, det).start()

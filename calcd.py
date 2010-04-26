## Module: calcd.py
## dumb calulator server


from socket import *
from calcsrv.config import *
from calcsrv.ProtocalHandler import ProtocalHandler
MAX_CONNS = 5 

srvsock = socket(AF_INET, SOCK_STREAM)

srvsock.bind((INET_ADDR, PORT))
srvsock.listen(MAX_CONNS)
print "Server Bound\n"

while True:
	chann, det = srvsock.accept()
	print str(det) + " Connected Starting ProtocalHandler\n"
	ProtocalHandler(chann, det).start()
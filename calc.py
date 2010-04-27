# Module: calc.py
# calcd client
# Matt Arnold

from socket import *
from sys import argv, exit

BUFFSIZE = 256
valid_ops = ["ADD", "SUB", "MUL", "DIV"]

if len(argv) != 3:
	print "Useage: " + argv[0] + "<host>" + "<PORT>"
	exit(-1)

clisock = socket(AF_INET, SOCK_STREAM)
remoteaddr = gethostbyname(argv[1])
port = int(argv[2])
print "Connecting to: " + remoteaddr + " " + str(port)
clisock.connect((remoteaddr, port))
clisock.send("INIT\n")
msg = clisock.recv(BUFFSIZE)
if msg.strip() != "OK":
	print "Init Error"
	exit(-1)


success_cnt = 0
while success_cnt < 2:

	out = raw_input("N>")
	if not out.isdigit():
		print "I'm not sending that"
		continue
	else:
		clisock.send(out + '\n')
	msg = clisock.recv(BUFFSIZE)
	if msg.strip() != "OK":
		print "Server Error try again"
	else:
		print "Ok next"
	
	success_cnt += 1

done = False

while not done:
	
	out = raw_input("OPP>")
	if not out in valid_ops:
		print "Not allowed by server"
		continue
	clisock.send(out + '\n')
	msg = clisock.recv(BUFFSIZE)
	if not msg.strip().isdigit():
		print "Server Error Try again"
	else:
		print msg.strip()
		done = True


clisock.close()
print "Goodbye"
exit(0)

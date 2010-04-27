## Protocal Handler for calcsrv
## Matt Arnold
# 4/26/10

from socket import *
from threading import *
from config import *

"""
supported_ops

A dict of all the operations this server supports
with expected msgs as keys and the python opertor as values
"""

supported_ops = {"ADD":"+", "SUB":"-","MUL":"*","DIV":"/"}

class ProtocalHandler(Thread):

	def __init__(self, conn, info):
		
		self.csock = conn
		self.cinfo = info
		self.junk = 0 ## No DoS thank you
		
		Thread.__init__(self) ## could use super but we want 2.5 compat
	
	def waitfornumber(self):
	
		while self.junk < ALLOWED_JUNK:
			
			msg = self.csock.recv(BUFFSIZE)
			proced_msg = msg.strip() # no newlines
			
			if proced_msg.isdigit():
				
				self.csock.send("OK\n")
				return proced_msg
			else:
				self.csock.send("NCK\n")
				self.junk += 1
			# end if-else
		# end while
		return 'E'
	# end def
	
	def waitforinit(self):
		
		while self.junk < ALLOWED_JUNK:
			
			msg = self.csock.recv(BUFFSIZE)
			proced_msg = msg.strip()
			
			if proced_msg == "INIT":
			
				self.csock.send("OK\n")
				return "O"
			else:
			
				self.csock.send("NCK\n")
				self.junk += 1
			# end if-else
		# end while
		return "E"
	# end def
	
	def waitforop(self):
		
		while self.junk < ALLOWED_JUNK:
		
			msg = self.csock.recv(BUFFSIZE)
			proced_msg = msg.strip()
			
			if proced_msg in supported_ops:
				
				return supported_ops[proced_msg]
			else:
				self.csock.send("NCK\n")
				self.junk += 1
			# end if-else
		# end while
		return "E"
	#end def
	
	def run(self):
		
		msg_li = ['E', 'E', 'E']
		init = self.waitforinit()
		if init != "O":
			self.csock.close()
			return
		# end if
		msg_li[0] = self.waitfornumber()
		msg_li[2] = self.waitfornumber()
		msg_li[1] = self.waitforop()
		
		if "E" not in msg_li:
			
			expr = ''.join(msg_li)
			finalresp = str(eval(expr)) + "\n"
			self.csock.send(finalresp)
		# endif
		self.csock.close()
	# enddef
# end class
		

## Protocal Handler for calcsrv
## Matt Arnold
## 4/26/10
## I've included some comments 
## for those new to python 
## which would otherwise violate
## python style conventions

from socket import *
from threading import *
from config import *

"""
supported_ops

A dict (same as Java HashMap) of all the operations this server supports
with expected msgs as keys and the python opertor as values
"""

supported_ops = {"ADD":"+", "SUB":"-","MUL":"*","DIV":"/"}

class ProtocalHandler(Thread):

	def __init__(self, conn, info):
		
		self.csock = conn
		self.cinfo = info
		self.junk = 0 ## a failsafe so we don't get DoSed
		## or DoS ourself by mistake
		
		Thread.__init__(self) ## could use super but we want 2.5 compat
	
	def waitfornumber(self):
	
		while self.junk < ALLOWED_JUNK:
			
			msg = self.csock.recv(BUFFSIZE)
			proced_msg = msg.strip() # if we don't strip \n's our
			# conditions will fail
			
			if proced_msg.isdigit(): # Accepting state
				
				self.csock.send("OK\n")
				self.junk = 0
				return proced_msg
			else:
				self.csock.send("NACK\n")
				self.junk += 1
			# end if-else
		# end while
		return ERR_STATE
	# end def
	
	def waitforinit(self):
		
		if active_count() > MAX_CONNS - 1:
			self.csock.send("BUSY\n")
			return ERR_STATE
		while self.junk < ALLOWED_JUNK:
			
			msg = self.csock.recv(BUFFSIZE)
			proced_msg = msg.strip().upper()
			
			if proced_msg == "INIT": # Accepting state
			
				self.csock.send("OK\n")
				self.junk = 0
				return OK_STATE
			else:
			
				self.csock.send("NACK\n")
				self.junk += 1
			# end if-else
		# end while
		return ERR_STATE
	# end def
	
	def waitforop(self):
		
		while self.junk < ALLOWED_JUNK:
		
			msg = self.csock.recv(BUFFSIZE)
			proced_msg = msg.strip().upper()
			
			if proced_msg in supported_ops: # hashmap lookup
				
				return supported_ops[proced_msg] 
				# return the value at that key 
				
			else:
				self.csock.send("NACK\n")
				self.junk += 1
			# end if-else
		# end while
		return ERR_STATE
	#end def
	
	def run(self):
		
		msg_li = [ERR_STATE, ERR_STATE, ERR_STATE] 
		# this list (sameas Java ArrayList)
		# Needs to be filled otherwise 
		# string joining won't work 
		# Correctly 
		init = self.waitforinit()
		if init != OK_STATE:
			self.csock.close()
			return
		# end if
		msg_li[0] = self.waitfornumber()
		msg_li[2] = self.waitfornumber()
		msg_li[1] = self.waitforop()
		
		if ERR_STATE not in msg_li:
			# if we get here all the other 
			# FSMs reached an accepting state
			# before DoS protection kicked in
			
			## Really cryptic trick here
			## I construct an anonymus
			## instance of the empty string
			## and join it with my list of string
			## producing a string 
			## that is a concatination of all three
			## i then tell the interperter to
			## evaluate said string as if it were 
			## in an assignment statement
			## and send the value that would
			## cross the = as a string followed by
			## \n
			expr = ''.join(msg_li)
			finalresp = str(eval(expr)) + "\n"
			self.csock.send(finalresp)
		# endif
		self.csock.close()
	# enddef
# end class
		

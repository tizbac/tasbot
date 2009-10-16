# -*- coding: utf-8 -*-
from socket import *
import string
import re
import time
import utilities
from utilities import *
from colors import *
import sys
import traceback
class User:
        def __init__(self,username,id,country,cpu):
                self.username = username
                self.id = id
                self.country = country
                self.cpu = cpu
                self.afk = False
                self.ingame = False
                self.mod = False
                self.rank = 0
                self.bot = False
        def clientstatus(self,status):
                self.afk = bool(getaway(int(status)))
                self.ingame = bool(getingame(int(status)))
                self.mod = bool(getmod(int(status)))
                self.bot = bool(getbot(int(status)))
                self.rank = getrank(status)-1
                
def parsecommand(cl,c,args,events,sock):
	if c.strip() != "":
		events.oncommandfromserver(c,args,sock)
		if c == "JOIN" and len(args) >= 1:
			if not args[0] in cl.channels:
				cl.channels.append(args[0])
				good("Joined #"+args[0])
		if c == "FORCELEAVECHANNEL" and len(args) >= 2:
			if args[0] in cl.channels:
				cl.channels.remove(args[0])
				bad("I've been kicked from #%s by <%s>" % (args[0],args[1]))
			else:
				error("I've been kicked from a channel that i haven't joined")
		if c == "TASSERVER":
			good("Connected to server")
			
			if cl.fl.register:
				cl.register(cl.uname,cl.password)
				receive(cl,sock,events)
			else:
				events.onconnected()
		if c == "AGREEMENTEND":
			notice("accepting agreement")
			sock.send("CONFIRMAGREEMENT\n")
			cl.login(cl.uname,cl.password,"BOT",2000)
			events.onloggedin(sock)
		if c == "MOTD":
			events.onmotd(" ".join(args))
		if c == "ACCEPTED":
			events.onloggedin(sock)
		if c == "DENIED" and ' '.join(args).lower().count("already") == 0:
			error("Login failed ( %s ), trying to register..." % ' '.join(args))
			notice("Closing Connection")
			sock.close()
			cl.fl.register = True			
			cl.connect(cl.lastserver,cl.lastport)
			
		if c == "REGISTRATIONACCEPTED":
			good("Registered")
			notice("Closing Connection")
			sock.close()
			cl.fl.register = False
			cl.connect(cl.lastserver,cl.lastport)
		if c == "PONG":
			cl.lpo = time.time()
			events.onpong()
		if c == "SAIDPRIVATE" and len(args) >= 2:
			events.onsaidprivate(args[0],' '.join(args[1:]))
		if c == "ADDUSER":
                        try:
                                if len(args) == 4:#Account id
                                        cl.users[args[0]] = User(args[0],int(args[3]),args[1],int(args[2]))
                                        #notice(args[0]+":"+args[3])
                                elif len(args) == 3:
                                        cl.users[args[0]] = User(args[0],int(-1),args[1],int(args[2]))
                                        #notice(args[0]+":"+"-1")
                                else:
                                        error("Invalid ADDUSER Command from server: %s %s"%(c,str(args)))
                        except:
                                error("Invalid ADDUSER Command from server: %s %s"%(c,str(args)))
                                print traceback.format_exc()
                if c == "REMOVEUSER":
                        if len(args) == 1:
                                if args[0] in cl.users:
                                        del cl.users[args[0]]
                                else:
                                        error("Invalid REMOVEUSER Command: no such user"+args[0])
                        else:
                                error("Invalid REMOVEUSER Command: not enough arguments")
                if c == "CLIENTSTATUS":
                        if len(args) == 2:
                                if args[0] in cl.users:
                                        try:
                                                cl.users[args[0]].clientstatus(int(args[1]))
                                        except:
                                                error("Malformed CLIENTSTATUS")
                                                print traceback.format_exc()
                                else:
                                        error("Invalid CLIENTSTATUS: No such user <%s>" % args[0])
                                
def receive(cl,socket,events): #return commandname & args
	buf = ""
	try:
		while not buf.strip("\r ").endswith("\n"):
			#print "Receiving incomplete command..."
			nbuf =  socket.recv(512)
			if len(nbuf) == 0:
				return 1
			buf += nbuf
			if len(buf) > 1024*200:
			  error("Buffer size exceeded!!!")
			  return 1
	except:
		error("Connection Broken")
		return 1 # Connection broken
	commands = buf.strip("\r ").split("\n")
	for cmd in commands:
		c = cmd.split(" ")[0].upper()
		args = cmd.split(" ")[1:]
		parsecommand(cl,c,args,events,socket)
	return 0
class serverevents:
	def onconnected(self):
		good("Connected to TASServer")
	def onconnectedplugin(self):
		good("Connected to TASServer")
	def ondisconnected(self):
		bad("Disconnected")
	def onmotd(self,content):
		print blue+"** MOTD ** "+content+normal
	def onsaid(self,channel,user,message):
		print cyan+"#"+channel+"\t<"+user+">"+normal+message
	def onsaidex(self,channel,user,message):
		print magenta+"#"+channel+"\t<"+user+">"+normal+message
	def onsaidprivate(self,user,message):
		print cyan+"$PRIVATE\t<"+user+">"+normal+message
	def onloggedin(self,socket):
		print blue+"Logged in."+normal
	def onpong(self):
		#print blue+"PONG"+normal
		pass
	def oncommandfromserver(self,command,args,socket):
		#print yellow+"From Server: "+str(command)+" Args: "+str(args)+normal
		pass
	def onexit(self):
	  pass
class flags:
	norecwait = False
	register = False


class tasclient:
	sock = 0
	fl = flags()
	er = 0
	lp = 0.0
	lpo = 0.0
	users = dict()
	def mainloop(self):
		while 1:
			if self.er == 1:
				raise SystemExit(0)
			try:
				
				#print "Waiting data from socket"
				result = receive(self,self.sock,self.events)
				#print "Received data"
				if result == 1:
					self.events.ondisconnected()
					self.users = dict()
					error("SERVER: Timed out, reconnecting in 40 secs")
					self.main.connected = False
					if not self.fl.norecwait:
						time.sleep(40.0)
						self.fl.norecwait = False
					try:
						self.sock.close()
					except:
						pass
					self.sock = socket(AF_INET,SOCK_STREAM)
					self.sock.settimeout(40)
					self.sock.connect((self.lastserver,int(self.lastport)))
					receive(self,self.sock,self.events)
					self.main.connected = True
					self.events.onconnectedplugin()
			except SystemExit:
				raise SystemExit(0)
			except:
				print red+"Command Error"
				print '-'*60
				traceback.print_exc(file=sys.stdout)
				print '-'*60
	def __init__(self,app):
		self.events = serverevents()
		self.main = app
		self.channels = []
	def connect(self,server,port):
		self.lastserver = server
		self.lastport = port
		
		while 1:
			try:
				self.sock = socket(AF_INET,SOCK_STREAM)
				self.sock.settimeout(40)
				self.sock.connect((server,int(port)))
				self.events.onconnectedplugin()
				if self.main.reg:
					notice("Registering nick")
					self.main.Register(self.main.config["nick"],self.main.config["password"])
				res = receive(self,self.sock,self.events)
				if not res == 1:
					return
			except SystemExit:
				raise SystemExit(0)
			except:
				self.main.connected = False
				error("Cannot connect, retrying in 40 secs...")
				print '-'*60
				traceback.print_exc(file=sys.stdout)
				print '-'*60
				if self.er == 1:
					raise SystemExit(0)
				time.sleep(40.0)
		
		
	def disconnect(self,hard=False):
		try:
			self.sock.send("EXIT\n")
		except:
			pass
		self.sock.close()
		self.sock = 0
	def login(self,username,password,client,cpu,lanip="*"):
		notice("Trying to login with username %s " % (username))
		#print "LOGIN %s %s %i * %s\n" % (username,password,cpu,client)
		try:
			self.sock.send("LOGIN %s %s %i %s %s\t0\t%s\n" % (username,password,cpu,lanip,client,"a"))
		except:
			error("Cannot send login command")
		self.uname = username
		self.password = password
		self.channels = []
		receive(self,self.sock,self.events)
	def register(self,username,password):
		try:
			notice("Trying to register account")
			self.sock.send("REGISTER %s %s\n" % (username,password))
		except:
			error("Cannot send register command")
	def leave(self,channel): #Leaves a channel
		if channel in self.channels:
			try:
				self.sock.send("LEAVE %s\n" % channel)
				self.channels.remove(channel)
			except:
				bad("Failed to send LEAVE command")
		else:
			bad("leave(%s) : Not in channel" % channel)
	def ping(self):
		if self.er == 1:
			return
		try:
			self.sock.send("PING\n")
			self.lp = time.time()
		except:
			error("Cannot send ping command")
	
			
		

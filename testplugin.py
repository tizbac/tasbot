from colors import *
import string
class Main:
  def onconnected(self):
	  print "onconnected()"
  def ondisconnected(self):
	  print "ondisconnected()"
  def onmotd(self,content):
	  print "onmotd(%s)" % (str(content))
  def onsaid(self,channel,user,message):
	  print "onsaid(%s,%s,%s)" % (str(channel),str(user),str(message))
  def onsaidex(self,channel,user,message):
	  print "onsaidex(%s,%s,%s)" % (str(channel),str(user),str(message))
  def onsaidprivate(self,user,message):
	  print "onsaidprivate(%s,%s)" % (str(user),str(message))
  def onloggedin(self,socket):
	  print "onloggedin(%s)" % (str(socket))
	  socket.send("JOIN main\n")
  def onpong(self):
	  print "onpong()"
  def oncommandfromserver(self,command,args,socket):
	  print "oncommandfromserver(%s,%s,%s)" % (str(command),str(args),str(socket))
  def onexit(self):
	  print "onexit()"

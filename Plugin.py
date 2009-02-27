from colors import *
import sys
import traceback
class plghandler:
	plugins = dict()
	def addplugin(self,name,tasc):
		try:
			code = __import__(name)
		except:
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60
			error("Cannot load plugin   "+name)
		
			return
		
		self.plugins.update([(name,code.Main())])
		self.plugins[name].sock = tasc.sock
		#print "Pluging %s has %s functions" % (name,str(dir(self.plugins[name])))
		
		try:
			if "onload" in dir(self.plugins[name]):
				self.plugins[name].onload(tasc)
		except:
			error("Cannot load plugin   "+name)
			print '-'*60
			traceback.print_exc(file=sys.stdout)
			print '-'*60
			return
		loaded("Plugin " + name)
	def onconnected(self):
		for plugin in self.plugins:
			try:
				if "onconnected" in dir(self.plugins[plugin]):
					self.plugins[plugin].onconnected()
			except SystemExit:
				raise SystemExit(0)
			except:
				error("PLUGIN ERROR")
				print '-'*60
				traceback.print_exc(file=sys.stdout)
				print '-'*60
	def ondisconnected(self):
		for plugin in self.plugins:
			try:
				if "ondisconnected" in dir(self.plugins[plugin]):
					self.plugins[plugin].ondisconnected()
			except SystemExit:
				raise SystemExit(0)
			except:
				error("PLUGIN ERROR")
				print '-'*60
				traceback.print_exc(file=sys.stdout)
				print '-'*60
	def onmotd(self,content):
		for plugin in self.plugins:
			try:
				if "onmotd" in dir(self.plugins[plugin]):
					self.plugins[plugin].onmotd(content)
			except SystemExit:
				raise SystemExit(0)
			except:
				error("PLUGIN ERROR")
				print '-'*60
				traceback.print_exc(file=sys.stdout)
				print '-'*60
	def onsaid(self,channel,user,message):
		for plugin in self.plugins:
			try:
				if "onsaid" in dir(self.plugins[plugin]):
					self.plugins[plugin].onsaid(channel,user,message)
			except SystemExit:
				raise SystemExit(0)
			except:
				error("PLUGIN ERROR")
				print '-'*60
				traceback.print_exc(file=sys.stdout)
				print '-'*60
	def onsaidex(self,channel,user,message):
		for plugin in self.plugins:
			try:
				if "onsaidex" in dir(self.plugins[plugin]):
					self.plugins[plugin].onsaidex(channel,user,message)
			except SystemExit:
				raise SystemExit(0)
			except:
				error("PLUGIN ERROR")
				print '-'*60
				traceback.print_exc(file=sys.stdout)
				print '-'*60
	def onsaidprivate(self,user,message):
		for plugin in self.plugins:
			try:
				if "onsaidprivate" in dir(self.plugins[plugin]):
					self.plugins[plugin].onsaidprivate(user,message)
			except SystemExit:
				raise SystemExit(0)
			except:
				error("PLUGIN ERROR")
				print '-'*60
				traceback.print_exc(file=sys.stdout)
				print '-'*60
	def onloggedin(self,socket):
		
		for plugin in self.plugins:
			
			try:
				
				if "onloggedin" in dir(self.plugins[plugin]):
					self.plugins[plugin].onloggedin(socket)
			except SystemExit:
				raise SystemExit(0)
			except:
				error("PLUGIN ERROR")
				print '-'*60
				traceback.print_exc(file=sys.stdout)
				print '-'*60
	def onpong(self):
		for plugin in self.plugins:
			try:
				if "onpong" in dir(self.plugins[plugin]):
					self.plugins[plugin].onpong()
			except SystemExit:
				raise SystemExit(0)
			except:
				error("PLUGIN ERROR")
				print '-'*60
				traceback.print_exc(file=sys.stdout)
				print '-'*60
	def oncommandfromserver(self,command,args,socket):
		
		for plugin in self.plugins:
			try:
				if "oncommandfromserver" in dir(self.plugins[plugin]):
					
					self.plugins[plugin].oncommandfromserver(command,args,socket)
					
			except SystemExit:
				raise SystemExit(0)	
			except:
				error("PLUGIN ERROR")
				print '-'*60
				traceback.print_exc(file=sys.stdout)
				print '-'*60

# !/usr/bin/env python
# -*- coding:utf-8 -*-  
import ConfigParser
import os
class Utils:
	def __init__(self,env=None):
		print(os.getcwd())
		cf = ConfigParser.ConfigParser()
		cf.read("lib/config/config.conf")
		self.host = cf.get(env, "host")
		self.root = cf.get(env, "root")
		self.password = cf.get(env, "password")
		self.db = cf.get(env, "db")
		self.proxyIpAddress = cf.get(env,'proxyIpAddress')
		self.proxyIpPath = cf.get(env,'proxyIpPath')
		self.proxyIpUpdatePath = cf.get(env, 'proxyIpUpdatePath')
		self.fromaddr=cf.get(env,'fromaddr')
		self.fromAddrPassword = cf.get(env, 'fromAddrPassword')
		self.toaddrs = cf.get(env, 'toaddrs')
		self.smtpaddr = cf.get(env, 'smtpaddr')
		pass


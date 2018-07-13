#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import os, sys, subprocess
import __opts__,opts
import __udhcpc__
from udhcpc_script_d import *


def do_dhcpc():

	if os.environ["action"] == "bound":

		params = ["interface","ip","domain","dns","router","subnet","action"]
		for p in params: 
			if not p in os.environ: return

		subprocess.run(["/sbin/ip","-4","addr","add",os.environ["ip"]+"/"+os.environ["subnet"],"dev",os.environ["interface"]])
		subprocess.run(["/sbin/ip","-4","route","add","default","via",os.environ["router"]])

		if not "staticResolvers" in __opts__.opt_vals:
			with open("/ram/etc/resolv.conf","w") as fd:
				print("search",os.environ["domain"],file=fd)
				for i in os.environ["dns"].split():
					print("nameserver",i,file=fd)

		os.makedirs("/ram/dhcp",exist_ok=True)
		with open("/ram/dhcp/"+os.environ["interface"],"w") as fd:
			for p in params:
				print(os.environ["interface"] + "_" + p + "=" + os.environ[p],file=fd)

		with open("/ram/addrs","w") as fd:
			print("4",os.environ["ip"]+"/"+os.environ["subnet"],os.environ["ip"],os.environ["subnet"],file=fd)

		with open("/ram/etc/hosts","w") as fd:
			print("127.0.0.1 localhost",file=fd)
			print(os.environ["ip"],__opts__.opt_vals["serverHostname"],file=fd)

		import firewall
		firewall.make_firewall()

		with open("/dev/console","w") as fd:
			print("IP Address:",os.environ["ip"]+"/"+os.environ["subnet"],"gw",os.environ["router"],file=fd)

		subprocess.run(["/sbin/init","5"])
		return

	if os.environ["action"] == "deconfig":
		if "interface" in os.environ:
			subprocess.run(["/sbin/ip","-4","addr","flush","dev",os.environ["interface"]])
		return

	for dfn in __udhcpc__.dhcpc_fns: dfn()




if len(sys.argv) > 1: 
	os.environ["action"] = sys.argv[1]
	do_dhcpc()

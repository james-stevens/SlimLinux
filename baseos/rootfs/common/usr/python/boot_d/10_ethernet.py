#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import os, subprocess
import __opts__,opts, slimlib

print ("BOOT: 10_ethernet")

subprocess.run(["/sbin/ip","link","set","eth0","up"])

dst="/ram/addrs"
slimlib.remove(dst)

max_mask = { "4":32, "6": 128 }
with open(__opts__.syscfg,"r") as sysfd:
	with open(dst,"w") as afd:
		lines = [ l.strip() for l in sysfd if l.startswith("static4IP=") or l.startswith("static6IP=") ]
		for l in lines:
			ipv=l[6]
			val=l[10:].strip('"').strip("'")
			ip=val.split("/")
			if len(ip)==1: ip.append(max_mask[ipv])
			sub=ip[0]+"/"+ip[1]
			print(ipv,sub,ip[0],ip[1],file=afd)
			subprocess.run(["/sbin/ip","-"+ipv,"addr","add",sub,"dev","eth0"])

for ipv in ["4","6"]:
	if "static"+ipv+"GW" in __opts__.opt_vals:
		subprocess.run(["/sbin/ip","-"+ipv,"route","add","default","via",__opts__.opt_vals["static4GW"]])

with open("/proc/sys/net/ipv4/tcp_max_syn_backlog","a") as fd: print("10000",file=fd)

with open("/proc/sys/net/core/somaxconn","a") as fd: print("10000",file=fd)

with open("/proc/sys/net/ipv4/tcp_fin_timeout","a") as fd: print("5",file=fd)

with open("/proc/sys/net/ipv4/tcp_mtu_probing","a") as fd: print("1",file=fd)

with open("/proc/sys/net/ipv4/tcp_base_mss","a") as fd: print("1280",file=fd)

import firewall
firewall.make_firewall()

with open("/ram/etc/resolv.conf","w") as fd:
	for x in __opts__.opt_vals["staticResolvers"].split():
		print(x,file=fd)

with open("/ram/etc/hosts","w") as fd:
	print("127.0.0.1 localhost",file=fd)
	if "static4IP" in __opts__.opt_vals:
		print(__opts__.opt_vals["static4IP"],__opts__.opt_vals["serverHostname"],file=fd)

with open(__opts__.syscfg,"r") as sysfd:
	lines = [ l[12:].strip().strip('"').strip("'") for l in sysfd if l.startswith("staticRoute=") ]
	for l in lines:
		a = l.split()
		if a[0].find(":") >= 0: ipv="6"
		else: ipv="4"
		subprocess.run(["/sbin/ip","-"+ipv,"route","add",a[0],"via",a[1]])

#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__, opts, slimlib

fw_fns = []

localports = ""

with open("/proc/sys/net/ipv4/ip_local_port_range","r") as fd:
	lines=[ l.strip() for l in fd ]

x = lines[0].split()
localports = x[0] + ":" + x[1]

def add_external_resolvers(ipv):
	dns=None
	if "staticResolvers" in __opts__.opt_vals:
		dns=__opts__.opt_vals["staticResolvers"]
	elif os.path.isfile("/ram/dhcp/eth0"):
		with open("/ram/dhcp/eth0","r") as fd:
			lines = [ l.split() for l in fd if l.startswith("eth0_dns=") ]
		dns=lines[0]
		dns=dns[dns.find("=")+1:]

	if dns == None:
		print("-A INPUT -p udp --sport 53 --dport "+localports+" -m state --state ESTABLISHED,RELATED -j ACCEPT")
		print("-A OUTPUT -p udp --dport 53 --sport "+localports+" -j ACCEPT")
	else:
		for all in slimlib.by_addr_type(dns,ipv):
			print("-A INPUT -p udp -s "+all+" --sport 53 --dport "+localports+" -m state --state ESTABLISHED,RELATED -j ACCEPT")
			print("-A OUTPUT -p udp -d "+all+" --dport 53 --sport "+localports+" -j ACCEPT")

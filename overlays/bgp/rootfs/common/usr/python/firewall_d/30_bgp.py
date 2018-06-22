#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import os
import __opts__,opts, __firewall__, slimlib


def fn_30_bgp(ipv):
	if not slimlib.opt_is_y("runningBGPd"): return

	print("-A BGPEER -p icmp -j ACCEPT")
	print("-A BGPEER -p tcp --dport 179 -j ACCEPT")
	print("-A BGPEER -p tcp --sport 179 -j ACCEPT")

	if os.path.isfile("/opt/config/bgpd.conf"):
		with open("/opt/config/bgpd.conf","r") as fd:
			addrs = [ l.strip().split()[2] for l in fd if l.startswith("neighbor ") and l.find(" remote-as ") >= 0 ]
	else:
		with open(__opts__.syscfg,"r") as fd:
			addrs= [ l[9:].strip('"').strip("'").split(",")[0] for l in fd if l.startswith("bgpPeers=") ]

	for ip in addrs:
		if select_addr(ip,ipv):
			print ("-A INPUT -s",ip,"-j BGPEER")
			print ("-A OUTPUT -d",ip,"-j BGPEER")

	if "bgpRemoteAllow" in __opts__.opt_vals:
		for all in slimlib.by_addr_type(__opts__.opt_vals["bgpRemoteAllow"],ipv):
			print("-A INPUT -p tcp -m tcp -s "+all+" --dport 2601 -j ACCEPT")
			print("-A INPUT -p tcp -m tcp -s "+all+" --dport 2605 -j ACCEPT")
			print("-A OUTPUT -p tcp -m tcp -d "+all+" --sport 2601 -j ACCEPT")
			print("-A OUTPUT -p tcp -m tcp -d "+all+" --sport 2605 -j ACCEPT")



__firewall__.fw_fns.append(fn_30_bgp)

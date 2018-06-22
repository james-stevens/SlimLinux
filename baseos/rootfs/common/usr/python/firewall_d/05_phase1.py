#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__,opts, slimlib
import __firewall__

def fn_05_phase1(ipv):

	print("-A INPUT -i lo -j ACCEPT")
	print("-A OUTPUT -o lo -j ACCEPT")

	if ipv == "4":
		print("-A INPUT -d 255.255.255.255 -j DROP")
		print("-A INPUT -d 224.0.0.1 -p 2 -j DROP")

	if ipv == "4" and "static4IP" not in __opts__.opt_vals:
		print("-A INPUT -p udp --sport 67 --dport 68 -j ACCEPT")

	icmp="icmp"
	if ""+ipv+"" == "6": icmp="icmpv6"

	if "pingAllow" in __opts__.opt_vals:
		for all in slimlib.by_addr_type(__opts__.opt_vals["pingAllow"],ipv):
			print("-A INPUT -p "+icmp+" -s "+all+" --"+icmp+"-type echo-request -j ACCEPT")
		print("-A INPUT -p "+icmp+" --"+icmp+"-type echo-request -j DROP")

	print("-A INPUT -p "+icmp+" -j ACCEPT")
	print("-A OUTPUT -p "+icmp+" -j ACCEPT")

	print("-A INPUT -p udp --dport 137 -j DROP")
	print("-A INPUT -p udp --dport 138 -j DROP")
	print("-A INPUT -p tcp --dport 135 -j DROP")
	print("-A INPUT -p tcp --dport 139 -j DROP")
	print("-A INPUT -p tcp --dport 445 -j DROP")


__firewall__.fw_fns.append(fn_05_phase1)

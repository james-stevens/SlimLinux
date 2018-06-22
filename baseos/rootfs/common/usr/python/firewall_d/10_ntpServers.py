#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__,opts, slimlib
import __firewall__

def fn_10_ntpServers(ipv):

	if "ntpServers" in __opts__.opt_vals:
		if "ntpAllow" in __opts__.opt_vals:
			for all in slimlib.by_addr_type(__opts__.opt_vals["ntpAllow"],ipv):
				print("-A INPUT -s "+all+" -p udp --dport 123 -j ACCEPT")
				print("-A OUTPUT -d "+all+" -p udp --sport 123 -j ACCEPT")

		print("-A INPUT -p udp --sport 123 --dport "+__firewall__.localports+" -m state --state ESTABLISHED,RELATED -j ACCEPT")
		print("-A OUTPUT -p udp --dport 123 --sport "+__firewall__.localports+" -j ACCEPT")


__firewall__.fw_fns.append(fn_10_ntpServers)

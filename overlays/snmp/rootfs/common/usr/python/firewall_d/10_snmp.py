#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__,opts, slimlib

if slimlib.opt_is_y("runningSnmpd"):
	if "snmpRemoteAllow" in __opts__.opt_vals:
		src=__opts__.opt_vals["snmpRemoteAllow"]
	else:
		src="0/0"

		for all in slimlib.by_addr_type(src):
			print("-A INPUT -p udp -m udp -s "+all+" --dport 161 -j ACCEPT")
			print("-A OUTPUT -p udp -m udp -d "+all+" --sport 161 -j ACCEPT")

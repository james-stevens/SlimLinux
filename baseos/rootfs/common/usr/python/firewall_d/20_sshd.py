#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__,opts, slimlib
import __firewall__

def fn_20_sshd(ipv):
	if slimlib.opt_is_y("runningSSHd"):
		if "sshRemoteAllow" in __opts__.opt_vals:
			for all in slimlib.by_addr_type(__opts__.opt_vals["sshRemoteAllow"],ipv):
				print("-A INPUT -p tcp -s "+all+" --dport 22 -j ACCEPT")
				print("-A OUTPUT -p tcp -d "+all+" --sport 22 -j ACCEPT")
		else:
			print("-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT")
			print("-A OUTPUT -p tcp -m tcp --sport 22 -j ACCEPT")

__firewall__.fw_fns.append(fn_20_sshd)

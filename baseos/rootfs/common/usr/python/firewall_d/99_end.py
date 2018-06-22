#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__,opts, slimlib
import __firewall__

def fn_99_end(ipv):
	if slimlib.opt_is_y("firewallLogging"):
		print("-A OUTPUT -j LOG --log-prefix <OUT>")
		print("-A INPUT -j LOG --log-prefix <INP>")
		
	print("-A INPUT -j DROP")
	print("-A FORWARD -j DROP")
	print("-A OUTPUT -j DROP")
	print("COMMIT")

__firewall__.fw_fns.append(fn_99_end)

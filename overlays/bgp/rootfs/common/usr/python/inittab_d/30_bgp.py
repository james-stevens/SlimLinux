#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__, opts, __inittab__, slimlib

def fn_30_bgp():
	if slimlib.opt_is_y("runningBGPd"):
		print("zba:45:respawn:/sbin/python -m start_zebra >/tmp/zebra.log 2>&1")
		print("bgp:5:respawn:/sbin/python -m start_bgpd >/tmp/zebra.log 2>&1")


__inittab__.inittab_fns.append(fn_30_bgp)

#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __firewall__

def fn_00_start_bgp(ipv):
	print(":BGPEER - [0:0]")

__firewall__.fw_fns.append(fn_00_start_bgp)

#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __firewall__

def fn_00_start(ipv):
	print("*filter")
	print(":INPUT ACCEPT [0:0]")
	print(":FORWARD ACCEPT [0:0]")
	print(":OUTPUT ACCEPT [0:0]")

__firewall__.fw_fns.append(fn_00_start)

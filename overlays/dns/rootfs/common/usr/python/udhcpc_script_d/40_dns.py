#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __udhcpc__

def fn_40_dns():
	if "action" in __udhcpc__.settings and __udhcpc__.settings["action"] == "bound":
		import add_as112_ips

__udhcpc__.dhcpc_fns.append(fn_40_dns)

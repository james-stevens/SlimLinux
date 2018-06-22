#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __inittab__

def fn_40_dns():
	print("nmd:5:respawn:/sbin/python -m start_dns 2>/tmp/dns.log 2>&1")

__inittab__.inittab_fns.append(fn_40_dns)

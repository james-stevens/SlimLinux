#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __inittab__

def fn_99_end():
	print ("Z99:5:wait:/sbin/python -m server_up >/tmp/server_up.log 2>&1")


__inittab__.inittab_fns.append(fn_99_end)

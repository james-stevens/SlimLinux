#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import time,os
import slimlib, __opts__, opts

slimlib.capture_entropy()

slimlib.remove("/ram/just-booted")

with open("/tmp/all_done.log","w") as fd: print(time.ctime(),file=fd)

with open("/dev/console","w") as fd:
	if slimlib.opt_is_y("allowConsoleLogin"):
		print("--------------- Press Atl-F2 to Login  ---------------",file=fd)
	else:
		print("------------------ Boot Complete ---------------------",file=fd)

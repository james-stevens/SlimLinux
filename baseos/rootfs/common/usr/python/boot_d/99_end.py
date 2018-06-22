#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__,opts, slimlib

print ("BOOT: 99_end")

if slimlib.opt_is_y("allowConsoleLogin"):
	print("--------------- Press Atl-F2 to Login  ---------------")
else:
	print("------------------ Boot Complete ---------------------")

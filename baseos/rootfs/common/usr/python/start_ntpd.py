#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import string, os
import __opts__,opts

if "ntpServers" in __opts__.opt_vals:
	svrs=__opts__.opt_vals["ntpServers"].split()
else:
	svrs=["pool.ntp.org"]

with open("/ram/etc/ntp.conf","w") as fd:
	for s in svrs: print("server ",s,file=fd)

flags="-nN"
if "ntpAllow" in __opts__.opt_vals: flags="-lnN"

os.execl("/sbin/ntpd","/sbin/ntpd",flags)

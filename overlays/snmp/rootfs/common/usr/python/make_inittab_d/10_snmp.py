#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__,opts, slimlib

if slimlib.opt_is_y("runningSnmpd"):
	print("sn:45:respawn:/sbin/python -m start_snmpd >/tmp/snmpd.log 2>&1")

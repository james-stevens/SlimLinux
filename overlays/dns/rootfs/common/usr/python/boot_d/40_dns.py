#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__,opts, slimlib

if slimlib.opt_is_y("dnsResolver"):
	with open("/ram/etc/resolv.conf","w") as fd:
		print("nameserver 127.0.0.1",file=fd)


if slimlib.opt_is_y("dnsWithAS112"):
	import add_as112_ips

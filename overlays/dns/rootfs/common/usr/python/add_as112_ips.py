#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import subprocess
import __opts__,opts, slimlib

if slimlib.opt_is_y("dnsWithAS112"):
	with open("/dev/null","w") as fd:
		for ip in ["192.175.48.1","192.175.48.6","192.175.48.42","192.31.196.1"]:
			subprocess.run(["/sbin/ip","-4","add","addr",ip+"/32","dev","eth0"],stdout=fd,stderr=fd)

		for ip in ["2620:4f:8000::1","2620:4f:8000::6","2620:4f:8000::42","2001:4:112::1"]:
			subprocess.run(["/sbin/ip","-6","addr","add",ip+"/128","dev","eth0"],stdout=fd,stderr=fd)

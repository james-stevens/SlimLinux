#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__, opts
import os, subprocess, shutil

if os.path.isfile("/opt/config/zebra.conf"):
	os.execl("/usr/sbin/zebra","/usr/sbin/zebra","-f","/opt/config/zebra.conf")

import __opts__,opts

cfg="/ram/etc/zebra.conf"
with open(cfg,"w") as fd:
	print("! zebra.conf",file=fd)
	print("hostname",__opts__.opt_vals["serverHostname"],file=fd)

	passwd="aa"
	if "bgpPassword" in __opts__.opt_vals: passwd = __opts__.opt_vals["bgpPassword"]
	
	print("password",passwd,file=fd)

	if "bgpEditPassword" in __opts__.opt_vals:
		print("enable password",__opts__.opt_vals["bgpEditPassword"],file=fd)

	print("interface lo",file=fd)
	print("interface eth0",file=fd)


shutil.chown(cfg,"quagga","quagga")
os.chmod(cfg,0o400)
os.execl("/usr/sbin/zebra","/usr/sbin/zebra","-f",cfg)

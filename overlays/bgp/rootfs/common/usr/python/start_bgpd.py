#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details
#

import os, subprocess

with open("/dev/null","w") as fd:
	subprocess.run(["/sbin/killall","bgpd"],stdout=fd,stderr=fd)

dst="/opt/config/bgpd.conf"
if os.path.isfile(dst):
	os.execl("/usr/sbin/bgpd","/usr/sbin/bgpd","-f",dst)

import bgpd_conf
bgpd_conf.make_bgpd_conf()

os.execl("/usr/sbin/bgpd","/usr/sbin/bgpd","-f","/ram/etc/bgpd.conf")

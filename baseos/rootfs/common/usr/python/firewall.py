#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __firewall__, slimlib
from firewall_d import *
import os, sys, tempfile, filecmp, subprocess


def make_firewall():
	save_out = sys.stdout

	for ipv in ["4","6"]:
		(tfd,tname) = tempfile.mkstemp()
		sys.stdout = os.fdopen(tfd,"w")
		for ffn in __firewall__.fw_fns: ffn(ipv)
		sys.stdout.close();

		if ipv=="4": cmd="iptables"
		else: cmd="ip6tables"

		dst="/ram/etc/ip"+ipv+"tables.conf"
		os.rename(tname,dst)
		with open(dst,"r") as fd:
			if subprocess.run(["/sbin/"+cmd+"-restore"],stdin=fd):
				bz=dst+".bz2"
				slimlib.remove(bz)
				subprocess.run(["/sbin/bzip2",dst])

	sys.stdout = save_out



#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

from opts_d import *
import __opts__

import subprocess

if "rdateServers" in __opts__.opt_vals and not "ntpServers" in __opts__.opt_vals:
	subprocess.run(["/sbin/rdate",__opts__.opt_vals["rdateServers"]])

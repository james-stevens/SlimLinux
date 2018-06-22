#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import sys,os.path
import __opts__

def fn_01_base():
	for fname in __opts__.cfgs:
		if not os.path.isfile(fname) : continue
		with open(fname,"r") as fd:
			lines = [ l.strip() for l in fd if not ((l=="") or (l[0]=='#') or (l.find("=")<0)) ]
			for l in lines:
				p = l.find("=")
				tag=l[0:p]
				val=l[p+1:].strip('"').strip("'")
				if tag == "extraUser" :
					u = val.split()
					val = val[len(u[0]):].lstrip()
					__opts__.opt_users[u[0]]=val
				elif tag == "staticRoute" : __opts__.opt_routes.append(val)
				elif tag.endswith("_keys"): __opts__.opt_keys.append(tag[:-5]+":"+val)
				else:
					__opts__.opt_vals[tag] = val

		if not "serverHostname" in __opts__.opt_vals:
			__opts__.opt_vals["serverHostname"]="slimlinux.exmaple.com"

		if not "staticResolvers" in __opts__.opt_vals:
			__opts__.opt_vals["staticResolvers"]="8.8.8.8 8.8.4.4 208.67.220.220 208.67.222.222"

__opts__.opt_fns.append(fn_01_base)

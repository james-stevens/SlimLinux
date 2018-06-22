#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__, slimlib, os

def fn_40_dns():
	if "dnsSecondary" in __opts__.opt_vals:
		__opts__.opt_vals["dnsWithSecondary"]="Y"

	if "dnsPrimary" in __opts__.opt_vals:
		__opts__.opt_vals["dnsWithPrimary"]="Y"

	dnsbase="/ram/dns"
	if  (   slimlib.opt_is_y("dnsLogging")
		and slimlib.opt_is_y("dnsWithSecondary")
		and slimlib.opt_is_y("dnsWithPrimary")
		):
		dnsbase="/opt/data/dns"

	__opts__.opt_vals["dnsbase"]=dnsbase
	os.makedirs(dnsbase,exist_ok=True)

__opts__.opt_fns.append(fn_40_dns)

#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __firewall__

def fn_40_dns(ipv):
	__firewall__.add_external_resolvers(ipv)

__firewall__.fw_fns.append(fn_40_dns)

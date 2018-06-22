#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details
#
# Also a lot lifted from RFC7534
# https://tools.ietf.org/html/rfc7534

import os, tempfile, shutil
import __opts__,opts, slimlib

def make_bgpd_conf():
	with open("/ram/addrs") as fd:
		lines=[ l.strip() for l in fd if l.startswith("4 ") ]

	first4ip=lines[0].split()[2]

	(tfd,tname) = tempfile.mkstemp()
	fd = os.fdopen(tfd,"w")

	print("! bgpd.conf\n!",file=fd)
	print("hostname",__opts__.opt_vals["serverHostname"],file=fd)

	passwd="aa"
	if "bgpPassword" in __opts__.opt_vals: passwd = __opts__.opt_vals["bgpPassword"]

	print("password",passwd,file=fd)

	if "bgpEditPassword" in __opts__.opt_vals:
		print("enable password",__opts__.opt_vals["bgpEditPassword"],file=fd)

	if slimlib.opt_is_y("bgpWithAS112"):
		print("!",file=fd)
		print("! Note that all AS112 nodes use the local Autonomous System Number",file=fd)
		print("! 112, and originate the IPv4 prefixes 192.175.48.0/24 and",file=fd)
		print("! 192.31.196.0/24 and the IPv6 prefixes 2620:4f:8000::/48 and",file=fd)
		print("! 2001:4:112::/48.\n",file=fd)
		
		print("! IPv4-only or IPv6-only AS112 nodes should omit advertisements",file=fd)
		print("! for address families they do not support.\n",file=fd)
		
		print("ip prefix-list AS112-v4 permit 192.175.48.0/24",file=fd)
		print("ip prefix-list AS112-v4 permit 192.31.196.0/24\n",file=fd)
		
		print("ipv6 prefix-list AS112-v6 permit 2620:4f:8000::/48",file=fd)
		print("ipv6 prefix-list AS112-v6 permit 2001:4:112::/48\n",file=fd)
		print("ip as-path access-list 1 permit ^$\n",file=fd)
		
		print("router bgp 112",file=fd)
		print("bgp router-id",first4ip,file=fd)
		print("network 192.175.48.0/24",file=fd)
		print("network 192.31.196.0/24\n",file=fd)
	else:
		print("router bgp",__opts__.opt_vals["bgpMyASN"],file=fd)
		print("bgp router-id",first4ip,file=fd)


	with open(__opts__.syscfg,"r") as sysfd:
		lines=[l.strip()[9:] for l in sysfd if l.startswith("bgpPeers=")]
		for l in lines:
			a = l.split(",")
			addr=a[0]
			del a[0]
			asn=a[0]
			del a[0]
			if slimlib.select_addr(addr,"4"):	
				filter_name="AS112-v4"
			else:
				filter_name="AS112-v6"

			print("neighbor",addr,"remote-as",asn,file=fd)
			print("neighbor",addr,"next-hop-self",file=fd)
			if slimlib.opt_is_y("bgpWithAS112"):
				print("neighbor",addr,"prefix-list",filter_name,"out",file=fd)
				print("neighbor",addr,"filter-list 1 out",file=fd)
			for x in a:
				print("neighbor",addr,x,file=fd)


	print("address-family ipv6 unicast",file=fd)
	if slimlib.opt_is_y("bgpWithAS112"):
		print("network 2620:4f:8000::/48",file=fd)
		print("network 2001:4:112::/48",file=fd)


	with open(__opts__.syscfg,"r") as sysfd:
		lines=[l.strip()[9:] for l in sysfd if l.startswith("bgpPeers=")]
		for l in lines:
			a = l.split(",")
			addr=a[0]
			del a[0]
			asn=a[0]
			del a[0]
			if slimlib.select_addr(addr,"6"):
				print("neighbor",addr,"activate",file=fd)
				if slimlib.opt_is_y("bgpWithAS112"):
					print("neighbor",addr,"prefix-list AS112-v6 out",file=fd)
					print("neighbor",addr,"filter-list 1 out",file=fd)
				for x in a:
					print("neighbor",addr,x,file=fd)

	fd.close()
	shutil.chown(tname,"quagga","quagga")
	os.chmod(tname,0o400)
	os.rename(tname,"/ram/etc/bgpd.conf")

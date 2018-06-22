#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details
#
# Also a lot lifted from RFC7534
# https://tools.ietf.org/html/rfc7534

import subprocess, syslog, os
import __opts__,opts

dnsbase=__opts__.opt_vals["dnsbase"]

if "serverAdmin" in __opts__.opt_vals:
	admin=__opts__.opt_vals["serverAdmin"]
	admin.replace("@",".")
else:
	admin="admin.exmaple.net"

os.makedirs(dnsbase+"/var/dns",exist_ok=True)

for x in ["net","arpa"]:
	full="hostname.as112."+x
	path=dnsbase+"/var/dns/db."+full

	with open(path,"w") as fd:
		print("; db.${full}",file=fd)
		print(";\n$TTL    1W\n",file=fd)
		print("@       SOA     ",__opts__.opt_vals["serverHostname"]+".",admin+". (",file=fd)
		print("         1               ; serial number",file=fd)
		print("         1W              ; refresh",file=fd)
		print("         1M              ; retry",file=fd)
		print("         1W              ; expire",file=fd)
		print("         1W )            ; negative caching TTL",file=fd)
		print(";\n         NS      blackhole.as112.arpa.\n;\n",file=fd)
		print("   TXT     \"See http://www.as112.net/ for more information.\"",file=fd)
		print(";",file=fd)

		if "serverLocation" in __opts__.opt_vals:
			print(" LOC",__opts__.opt_vals["serverLocation"],file=fd)
			if (   "serverFacility" in __opts__.opt_vals 
				and "serverLocDesc" in __opts__.opt_vals
				):
				print("   TXT     \""+__opts__.opt_vals["serverFacility"]+"\" \""+__opts__.opt_vals["serverLocDesc"]+"\"",file=fd)

	if not subprocess.run(["/sbin/named-checkzone","-q",full,path]).returncode == 0:
		syslog.syslog("ERROR: ",full," failed validation checks")

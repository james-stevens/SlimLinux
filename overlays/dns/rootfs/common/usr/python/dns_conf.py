#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details
#
# Also a lot lifted from RFC7534
# https://tools.ietf.org/html/rfc7534

import __opts__,opts, slimlib, syslog
import tempfile, subprocess, os, shutil, random


def make_dns_conf():
	dnsbase=__opts__.opt_vals["dnsbase"]

	(ux_fd,tname) = tempfile.mkstemp()
	tfd = os.fdopen(ux_fd,"w")

	print("""options {
	   listen-on {
		   127.0.0.1;         // localhost

		 // The following address is node-dependent and should be set to
		 // something appropriate for the new AS112 node.

	""",file=tfd)

	with open("/ram/addrs","r") as fd:
		lines=[ l.split()[2] for l in fd if l.startswith("4 ") ]
	if len(lines) > 0: print("; ".join(lines),";",file=tfd)


	if slimlib.opt_is_y("dnsWithAS112"):
		print("""
		 // The following addresses are used to support Direct Delegation
		 // AS112 service and are the same for all AS112 nodes.

		   192.175.48.1;      // prisoner.iana.org (anycast)
		   192.175.48.6;      // blackhole-1.iana.org (anycast)
		   192.175.48.42;     // blackhole-2.iana.org (anycast)

		 // The following address is used to support DNAME redirection
		 // AS112 service and is the same for all AS112 nodes.

		   192.31.196.1;      // blackhole.as112.arpa (anycast)""",file=tfd)

	print("""};

		 listen-on-v6 {
		   ::1;               // localhost
	   """,file=tfd)

	if slimlib.opt_is_y("dnsWithAS112"):
		print("""
		 // The following addresses are used to support Direct Delegation
		 // AS112 service and are the same for all AS112 nodes.

		   2620:4f:8000::1;   // prisoner.iana.org (anycast)
		   2620:4f:8000::6;   // blackhole-1.iana.org (anycast)
		   2620:4f:8000::42;  // blackhole-2.iana.org (anycast)

		 // The following address is used to support DNAME redirection
		 // AS112 service and is the same for all AS112 nodes.

		   2001:4:112::1;    // blackhole.as112.arpa (anycast)
		   """,file=tfd)


	with open("/ram/addrs","r") as fd:
		lines=[ l.strip() for l in fd if l.startswith("6 ") ]
	if len(lines) > 0: print("; ".join(lines),";",file=tfd)

	print("""
		 };

		 directory "/var/dns";
		 allow-update { none; };
		 allow-transfer { 127.0.0.0/8; };
		 notify no;
		 max-udp-size 4096;
		 edns-udp-size 4096;
		""",file=tfd)


	if slimlib.opt_is_y("dnsDNSSEC"):
		print("dnssec-enable yes;",file=tfd)
	else:
		print("dnssec-enable no;",file=tfd)


	if slimlib.opt_is_y("dnsResolver"):
		print("    recursion yes;",file=tfd)
		if "dnsResolverAllowed" in __opts__.opt_vals:
			tfd.write("    allow-recursion { 127.0.0.0/8; ::1; ")
			for svr in __opts__.opt_vals["dnsResolverAllowed"].split(): tfd.write(svr+"; ")
			print("};",file=tfd)
	else:
		print("    recursion no;        // authoritative-only server",file=tfd)
		 
	print(" };  ",file=tfd)

	if slimlib.opt_is_y("dnsLogging"):
		print("// dnsLogging = ",__opts__.opt_vals["dnsLogging"],file=tfd)
		print("""
	   // Log queries, so that when people call us about unexpected
	   // answers to queries they did not realise they had sent, we
	   // have something to talk about.  Note that activating this
	   // naively has the potential to create high CPU load and consume
	   // enormous amounts of disk space.  This example retains 2 old
	   // versions at a maximum of 500 MB each before rotating out the
	   // oldest one.

	logging {
		 channel "querylog" {
		   file "/var/log/query.log" versions 2 size 500m;
		   print-time yes;
		 };
		 category queries { querylog; };
	   };""",file=tfd)



	if os.path.isfile("/opt/config/rndc.conf"):
		shutil.copy2("/opt/config/rndc.conf","/ram/etc/rndc.conf")
	elif "dnsRndcKey" in __opts__.opt_vals:
		print("key \"rndc-key\" { algorithm hmac-md5; secret \""+__opts__.opt_vals["dnsRndcKey"]+"\"; };",file=tfd)
		print("controls {",file=tfd)
		print("   inet 127.0.0.1 port 953 allow { 127.0.0.1; } keys { \"rndc-key\"; };",file=tfd)
		
		if ( "dnsRndcAllow" in __opts__.opt_vals 
			and not __opts__.opt_vals["dnsRndcAllow"] == "127.0.0.1"
			):
			addrs = __opts__.opt_vals["dnsRndcAllow"].split()
			for ipv in ["4","6"]:
				with open("/ram/addrs","r") as afd:
					lines=[ l.strip() for l in afd if l.startswith(ipv+" ") ]
				for l in lines:
					print("\tinet",l.split()[2],"port 953 allow {",file=tfd)

					for a in addrs:
						if slimlib.select_addr(a,ipv): tfd.write(a+"; ")

					print("} keys { \"rndc-key\"; };",file=tfd)

		print("};",file=tfd)

		with open("/ram/etc/rndc.conf","w") as rfd:
			print("key \"rndc-key\" { algorithm hmac-md5; secret \""+__opts__.opt_vals["dnsRndcKey"]+"\"; };",file=rfd)
			print("options { default-key \"rndc-key\"; default-server 127.0.0.1; default-port 953; };",file=rfd)



	if slimlib.opt_is_y("dnsWithAS112"):
		print("""
	   // Direct Delegation AS112 Service

	   // RFC 1918

	zone "10.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "16.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "17.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "18.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "19.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "20.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "21.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "22.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "23.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "24.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "25.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "26.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "27.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "28.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "29.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "30.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "31.172.in-addr.arpa" { type master; file "db.dd-empty"; };
	zone "168.192.in-addr.arpa" { type master; file "db.dd-empty"; };

	   // RFC 6890

	zone "254.169.in-addr.arpa" { type master; file "db.dd-empty"; };

	   // DNAME redirection AS112 Service

	zone "empty.as112.arpa" { type master; file "db.dr-empty"; };

	   // Also answer authoritatively for the HOSTNAME.AS112.NET and
	   // HOSTNAME.AS112.ARPA zones, which contain data of operational
	   // relevance.

	zone "hostname.as112.net" {
		 type master;
		 file "db.hostname.as112.net";
	   };

	zone "hostname.as112.arpa" {
		 type master;
		 file "db.hostname.as112.arpa";
	   };
	   """,file=tfd)



	if slimlib.opt_is_y("dnsWithSecondary"):
		os.makedirs(dnsbase+"/slave",exist_ok=True)

		shutil.chown(dnsbase+"/slave","nobody","nobody")

		with open(__opts__.syscfg,"r") as sysfd:
			lines = [ l.strip()[13:].strip('"').strip("'") for l in sysfd if l.startswith("dnsSecondary=") ]
			for l in lines:
				a = l.split()
				file=a[0].replace("/","_").replace(":","_")
				tfd.write("zone \""+a[0]+"\"  { type slave; file \"/slave/"+file+"\";\n\tmasters {")
				del a[0]
				tfd.write("; ".join(a))

				print("; }; };\n",file=tfd)



	if slimlib.opt_is_y("dnsWithPrimary"):
		os.makedirs(dnsbase+"/master",exist_ok=True)

		shutil.chown(dnsbase+"/slave","nobody","nobody")

		with open(__opts__.syscfg,"r") as sysfd:
			lines = [ l.strip()[11:].strip('"').strip("'") for l in sysfd if l.startswith("dnsPrimary=") ]
			for l in lines:
				a = l.split()
				file=a[0].replace("/","_").replace(":","_")
				tfd.write("zone \""+a[0]+"\"  { type master; notify explicit; file \"/slave/"+file+"\";\n\tmasters {")
				del a[0]
				iplist = [ l.strip() for l in a if l.find("/") < 0 ]
				tfd.write("\tallow-transfer { "+"; ".join(a)+"; 127.0.0.0/8; };\n")
				tfd.write("\talso-notify { "+"; ".join(iplist)+"; };\n")
				print("\t};\n",file=tfd)

	tfd.close()
	conf="/etc/dns.conf"
	dst=dnsbase+conf
	os.makedirs(dnsbase+"/etc",exist_ok=True)

	tmp=dnsbase+conf+"_"+str(os.getpid())+"_"+str(random.randint(1,100000))
	shutil.copy2(tname,tmp)
	slimlib.remove(tname)
	shutil.chown(tmp,"nobody","nobody")
	os.chmod(tmp,0o400)
	os.rename(tmp,dst)

	if not subprocess.run(["/sbin/named-checkconf","-t",dnsbase,conf]).returncode == 0:
		syslog.syslog("ERROR: \""+conf+"\" failed validation checks")
	else:
		subprocess.run(["/sbin/killall","-q","-HUP","named"])

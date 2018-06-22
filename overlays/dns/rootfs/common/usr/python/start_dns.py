#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import os, shutil, syslog, subprocess, stat, syslog
import __opts__,opts, slimlib


def make_dev(path,major,minor):
	try:
		os.remove(path)
	except:
		pass
	os.mknod(path,stat.S_IFCHR,device=os.makedev(major,minor))
	os.chmod(path,0o666)


dnsbase=__opts__.opt_vals["dnsbase"]
os.makedirs(dnsbase,exist_ok=True)
os.chdir(dnsbase)

os.makedirs("dev",exist_ok=True)
make_dev("dev/null",1,3)
make_dev("dev/random",1,8)
make_dev("dev/urandom",1,9)
make_dev("dev/zero",1,5)
os.makedirs("etc",exist_ok=True)

for dir in ["var","var/dns","var/log","var/run","var/run/dns"]: os.makedirs(dir,exist_ok=True)

for dir in ["var/log","var/run","var/run/dns"]: os.chmod(dir,0o777)

for dir in ["dev","var","etc"]: os.chmod(dir,0o755)

shutil.chown("var/dns","nobody","nobody")

if slimlib.opt_is_y("dnsWithAS112"):
	import make_db_hostname_as112
	shutil.copy2("/opt/dns/etc/db.as112.arpa","var/dns")
	shutil.copy2("/opt/dns/etc/db.dd-empty","var/dns")
	shutil.copy2("/opt/dns/etc/db.dr-empty","var/dns")


conf="/etc/dns.conf"
path=dnsbase+conf
if os.path.isfile("/opt/config/dns.conf"):
	if os.path.isfile(path): os.remove(path)
	shutil.copy2("opt/config/dns.conf",path)
	os.chmod(path,0o600)
	shutil.chown(path,"nobody","nobody")
else:
	import dns_conf
	dns_conf.make_dns_conf()


if not subprocess.run(["/sbin/named-checkconf","-t",dnsbase,conf]).returncode == 0:
	syslog.syslog("dns.conf failed named-checkconf")
	os.execl("/bin/sleep","/bin/sleep","911")


os.execl("/usr/sbin/named","/usr/sbin/named","-u","nobody","-t",dnsbase,"-f","-c",conf)


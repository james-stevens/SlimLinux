#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import os, subprocess
import __opts__,opts

os.makedirs("/ram/net-snmp",exist_ok=True)

subprocess.run(["/sbin/killall","-q","snmpd"])

if os.path.isfile("/opt/config/snmpd.conf"):
	os.execl("/usr/sbin/snmpd","/usr/sbin/snmpd","-u","nobody","-r","-f","-c","/opt/config/snmpd.conf")


with open("/ram/etc/snmpd.conf","w") as fd:
	print("""com2sec   public    default       public

group  worldGroup  v1         public
group  worldGroup  v2c        public
group  myGroup     v1         mynet
group  myGroup     v2c        mynet

view   sysView included    system
view   sysView included    .1.3.6.1.2.1.25.1
view   sysView included    .1.3.6.1.2.1.2.2.1

access  worldGroup  \"\"  any  noauth  exact   sysView  none   none""",file=fd)


os.execl("/usr/sbin/snmpd","/usr/sbin/snmpd","-u","nobody","-r","-f","-c","/ram/etc/snmpd.conf")

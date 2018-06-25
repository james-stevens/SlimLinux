#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import os, stat, subprocess, tempfile
import __opts__,opts,slimlib

os.makedirs("/ram/ssh",exist_ok=True)

with open("/ram/ssh/moduli","w") as fd:
	subprocess.run(["/sbin/xz","-dc","/etc/moduli.xz"],stdout=fd)


store="/opt/config/ssh"

if os.path.isdir(store):
	slimlib.copytree(store,"/ram/ssh")
else:
	subprocess.run(["/sbin/ssh-keygen","-A"])
	os.makedirs(store,exist_ok=True)
	slimlib.copytree("/ram/ssh",store)


if not os.path.isdir("/opt/config/ssh/sshd_config"):
	(tfd,tname) = tempfile.mkstemp()
	myf = os.fdopen(tfd,"w")

	if os.path.isdir("/etc/pam.d/."):
		print("UsePAM yes",file=myf)

	if slimlib.opt_is_y("allowRootSSH"):
		print("PermitRootLogin Yes",file=myf)

	print("PubkeyAcceptedKeyTypes=+ssh-dss,ssh-rsa",file=myf)
	myf.close()

	os.chmod(tname,stat.S_IRUSR)
	os.rename(tname,"/ram/ssh/sshd_config")
	slimlib.remove(tname)


os.execl("/usr/sbin/sshd","/usr/sbin/sshd","-D")

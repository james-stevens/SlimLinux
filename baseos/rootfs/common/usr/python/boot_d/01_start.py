#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import subprocess, os, shutil, stat
from subprocess import Popen, PIPE

print("BOOT: 01_start")

subprocess.run(["/sbin/dmesg","-n","5"])

subprocess.run(["/sbin/mount","-o","noexec","-t","proc","/proc","/proc"])
subprocess.run(["/sbin/mount","-o","noexec","-t","sysfs","/sys","/sys"])

if not os.path.isdir("/dev/pts"): os.mkdir("/dev/pts")
subprocess.run(["/sbin/mount","-o","noexec","-t","devpts","/dev/pts","/dev/pts"])

subprocess.run(["/sbin/fsck","-A","-y"])

subprocess.run(["/sbin/mount","-a"])
subprocess.run(["/sbin/mount","-ro","remount,noatime","/"])
subprocess.run(["/sbin/mount","-t","tmpfs","-o","noexec,size=3M","RamDISK","/ram"])


import slimlib
if os.path.isdir("/etc/config") and not os.path.isfile("/opt/config/system.cfg"):
	slimlib.copytree("/etc/config","/opt/config")

import __opts__
dst=__opts__.syscfg
dir="/etc/base_config"

if not os.path.isfile(dst):
	files = os.listdir(dir)
	with open(dst,"w") as mfd:
		for file in files:
			with open(dir+"/"+file,"r") as tfd:
				lines = [line.rstrip() for line in tfd] 
			mfd.write("\n".join(lines))

import opts

rnd="/opt/config/seed.rnd"
if os.path.isfile(rnd):
	with open(rnd,"rb") as fd:
		data=fd.read()
		with open("/dev/urandom","ab") as rfd:
			rfd.write(data)

for dir in ["ssh","root","tmp","etc","var","var/run","var/db","var/lib"]: 
	os.mkdir("/ram/"+dir)

os.chmod("/ram/tmp",0o777+stat.S_ISVTX)
os.chmod("/ram/var/run",0o777+stat.S_ISVTX)
open("/ram/etc/adjtime",'a').close()

for f in [__opts__.syscfg,"/ram/ssh","/ram/root"]: 
	os.chown(f,0,0)
	os.chmod(f,0o700)

if os.path.isfile("/opt/config/busybox.conf"):
	os.symlink("/opt/config/busybox.conf","/ram/etc/busybox.conf")
else:
	open("/ram/etc/busybox.conf",'a').close()

open("/ram/just-booted",'a').close()

subprocess.run(["/sbin/ip","link","set","lo","up"])

os.makedirs("/opt/data/log",exist_ok=True)
for f in ["/var/log/lastlog","/var/log/wtmp"]: open(f,'a').close()

import inittab
inittab.make_inittab()
import make_shadow

opts.remake_opts()

subprocess.run(["/sbin/hostname",__opts__.opt_vals["serverHostname"]])

mapfile="/etc/kmap/uk.bmap.gz"

if "keyboardMap" in __opts__.opt_vals and os.path.isfile("/etc/kmap/"+__opts__.opt_vals["keyboardMap"]+".bmap.gz"):
	mapfile="/etc/kmap/"+__opts__.opt_vals["keyboardMap"]+".bmap.gz"

p = Popen(["/sbin/zcat",mapfile],stdout=PIPE)
data = p.stdout.read()
p.wait()
p = Popen(["/sbin/loadkmap"],stdin=PIPE)
p.stdin.write(data)
p.stdin.close()
p.wait()


if "baseos" in __opts__.opt_vals:
	desc=__opts__.opt_vals["baseos"]+": "
	if "overlays" in __opts__.opt_vals:
		desc=desc+__opts__.opt_vals["overlays"]
else:
	desc="SlimLinux"

with open("/proc/version") as fd:
	lines = [line.rstrip() for line in fd] 
	r = lines[0].split()

with open("/ram/etc/motd","w") as motd:
	print("",file=motd)
	print(desc,file=motd)
	print("Kernel "+r[0]+" "+r[1]+" "+r[2],file=motd)

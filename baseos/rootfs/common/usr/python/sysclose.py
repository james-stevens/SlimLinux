#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import sys, subprocess, time, os
import slimlib

def do_sys_close(end_cmd):
	slimlib.capture_entropy()

	subprocess.run(["/sbin/killall5","-15"])
	time.sleep(3)
	subprocess.run(["/sbin/killall5","-9"])

	subprocess.run(["/sbin/swapoff","-a"])
	os.sync()
	subprocess.run(["/sbin/umount","-a"])
	subprocess.run(["/sbin/mount","-v","-no","remount,ro","/"])
	os.sync()
	print("Running -",end_cmd)
	subprocess.run(["/sbin/"+end_cmd,"-f"])

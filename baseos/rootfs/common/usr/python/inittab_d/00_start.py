#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__, opts, __inittab__, slimlib



def fn_00_start():
	deflevel="2"
	if "static4IP" in __opts__.opt_vals: deflevel="5"

	print("id:"+deflevel+":initdefault:")

	print ("")
	print ("si:S:sysinit:/sbin/python -m boot")
	print ("ca::ctrlaltdel:/sbin/init 6")
	print ("l0:0:wait:/sbin/python -m poweroff")
	print ("l6:6:wait:/sbin/python -m reboot")
	print ("")

	print("hd:2345:respawn:/usr/sbin/haveged -F >/tmp/haveged.log 2>&1")

	if slimlib.opt_is_y("allowConsoleLogin"):
		print ("c2:12345:respawn:/sbin/getty 38400 tty2 linux")
		print ("c3:12345:respawn:/sbin/getty 38400 tty3 linux")
		print ("c4:12345:respawn:/sbin/getty 38400 tty4 linux")

	# print ("X5:12345:respawn:/sbin/sh < /dev/tty5 > /dev/tty5 2>&1")
	# print ("X6:12345:respawn:/sbin/sh < /dev/tty6 > /dev/tty6 2>&1")
	# print ("X7:12345:respawn:/sbin/sh < /dev/tty7 > /dev/tty7 2>&1")

	print ("")

	if slimlib.opt_is_y("syslogToDisk"):
		extra_syslog=""
		if "syslogSize" in __opts__.opt_vals:
			extra_syslog="-s " + __opts__.opt_vals["syslogSize"]
		print("sl:2345:respawn:/sbin/syslogd -n -b 5 -D",extra_syslog)
	else:
		print("sl:2345:respawn:/sbin/syslogd -n -C100")

	print ("kl:2345:respawn:/sbin/klogd -n")
	print ("ap:2345:respawn:/sbin/acpid -d -f >/dev/tty9 2>&1")

	print ("")

	if not "static4IP" in __opts__.opt_vals:
		print ("dh:2345:respawn:/sbin/udhcpc -f -s /usr/python/udhcpc_script.py -S >/tmp/udhcpc.log 2>&1")

	print ("")
	print ("cr:345:respawn:/sbin/crond -l 10 -c /var/cron -f")

	# allow some entropy to accumulate before running sshd
	print ("wt:345:wait:/sbin/sleep 0.5")

	if "ntpServers"in __opts__.opt_vals:
		print ("ntp:345:respawn:/sbin/python -m start_ntpd > /tmp/ntpd.log 2>&1")

	if slimlib.opt_is_y("runningSSHd"):
		print ("sd:345:respawn:/sbin/python -m start_sshd > /tmp/sshd.log 2>&1")


__inittab__.inittab_fns.append(fn_00_start)

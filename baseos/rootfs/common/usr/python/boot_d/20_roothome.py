#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import shutil, os
import __opts__,opts
import make_auth_keys

print ("BOOT: 20_roothome")

shutil.copy2("/etc/root_profile","/ram/root/.profile")

with open("/ram/root/.profile","a") as fd:
	print("if tty -s ; then echo -ne '\\e]2;"+__opts__.opt_vals["serverHostname"]+"\\a'; fi",file=fd)

make_auth_keys.root()

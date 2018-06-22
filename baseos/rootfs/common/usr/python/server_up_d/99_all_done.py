#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import datetime,os
import slimlib

slimlib.capture_entropy()

os.unlink("/ram/just-booted")

with open("/tmp/all_done.log","w") as fd: print(datetime.ctime(),file=fd)

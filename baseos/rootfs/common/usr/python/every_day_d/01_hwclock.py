#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import subprocess

subprocess.run(["/sbin/hwclock","-w","-u"])

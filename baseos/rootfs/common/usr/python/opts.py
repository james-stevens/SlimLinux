#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

from opts_d import *
import __opts__

def remake_opts():
	__opts__.opt_vals.clear()
	for ofn in __opts__.opt_fns: ofn()

remake_opts()

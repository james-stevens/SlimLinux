#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import os, sys, filecmp, tempfile, signal
import __inittab__
from inittab_d import *


def make_inittab():
	save_out = sys.stdout
	(tfd,tname) = tempfile.mkstemp()
	sys.stdout = os.fdopen(tfd,"w")
	for ifn in __inittab__.inittab_fns: ifn()
	sys.stdout.close();
	sys.stdout = save_out

	dst="/ram/etc/inittab"
	if not os.path.isfile(dst) or not filecmp.cmp(tname,dst,False):
		os.rename(tname,dst)
		os.kill(1,signal.SIGHUP)

	if os.path.isfile(tname): os.unlink(tname)

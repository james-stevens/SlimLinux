#! /sbin/python
#
# Parts (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import os
from shutil import copy2, copystat
import __opts__

#
# this is a copy of "copytree" from "shutil" (comments removed),
# but allows the dst-dir to not exist
#
def copytree(src, dst, symlinks=False, ignore=None, copy_function=copy2,
			 ignore_dangling_symlinks=False):
	names = os.listdir(src)
	if ignore is not None:
		ignored_names = ignore(src, names)
	else:
		ignored_names = set()

	###########################################
	# ==> next line added "exist_ok=True" <== #
	###########################################
	os.makedirs(dst,exist_ok=True)

	errors = []
	for name in names:
		if name in ignored_names:
			continue
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)
		try:
			if os.path.islink(srcname):
				linkto = os.readlink(srcname)
				if symlinks:
					os.symlink(linkto, dstname)
					copystat(srcname, dstname, follow_symlinks=not symlinks)
				else:
					if not os.path.exists(linkto) and ignore_dangling_symlinks:
						continue
					if os.path.isdir(srcname):
						copytree(srcname, dstname, symlinks, ignore,
								 copy_function)
					else:
						copy_function(srcname, dstname)
			elif os.path.isdir(srcname):
				copytree(srcname, dstname, symlinks, ignore, copy_function)
			else:
				copy_function(srcname, dstname)
		except Error as err:
			errors.extend(err.args[0])
		except OSError as why:
			errors.append((srcname, dstname, str(why)))
	try:
		copystat(src, dst)
	except OSError as why:
		if getattr(why, 'winerror', None) is None:
			errors.append((src, dst, str(why)))
	if errors:
		raise Error(errors)
	return dst



def select_addr(a,ipv):
	if a.find(":") >=0: return (ipv=="6")
	else: return (ipv=="4")


def by_addr_type(addrs,ipv):
	return [ a  for a in addrs.split() if select_addr(a,ipv) ]


def capture_entropy():
	with open("/dev/urandom","rb") as fd:
		data = fd.read(512)
		with open("/opt/config/seed.rnd","wb") as sfd:
			sfd.write(data)

def opt_is_y(tag):
	return tag in __opts__.opt_vals and __opts__.opt_vals[tag]=="Y"

def remove(path):
	try:
		os.remove(path)
	except:
		pass

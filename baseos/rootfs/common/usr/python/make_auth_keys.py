#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__,opts
import os,stat

def user(user,u,g):
	dst="/ram/home"
	for x in ["/"+user,"/.ssh"]:
		dst=dst+x
		if not os.path.isdir(dst): 
			os.mkdir(dst)
			os.chown(dst,u,g)

	dst=dst+"/authorized_keys"
	kfd=open(dst,"w")

	for x in __opts__.opt_keys:
		k = x.split(":")
		if k[0]=="user" or k[0]=="auth" or k[0]==user: print(k[1],file=kfd)

	kfd.close()
	os.chmod(dst,stat.S_IRUSR)
	os.chown(dst,u,g)



def root():
	dst="/ram/root/.ssh"
	if not os.path.isdir(dst): os.mkdir(dst)
	dst=dst+"/authorized_keys"

	kfd=open(dst,"w")

	for x in __opts__.opt_keys:
		k = x.split(":")
		if k[0]=="auth" or k[0]=="auth": print(k[1],file=kfd)

	kfd.close()
	os.chmod(dst,stat.S_IRUSR)

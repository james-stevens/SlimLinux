#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__,opts
import stat, os, shutil
import make_auth_keys

make_auth_keys.root()

sfd = open("/ram/etc/shadow","w")
pfd = open("/ram/etc/passwd","w")

rootpass="IApiqCICbjOKo"
if "rootPassword" in __opts__.opt_vals:
	rootpass=__opts__.opt_vals["rootPassword"]

print("root:"+rootpass+":16750:0:::::",file=sfd)

print("root:x:0:0::/ram/root:/bin/sh",file=pfd)
print("sshd:x:33:33::/tmp:/bin/false",file=pfd)
print("nobody:x:9999:9999::/tmp:/bin/false",file=pfd)



grps = {}
grp_ids = {}
grp_ids["users"]=100
grp_ids["sudo"]=20

uids=100
for user in __opts__.opt_users:
	r = __opts__.opt_users[user].split()

	if len(r) > 1:
		uid = r[1]
	else:
		uid=uids;
		uids += 1

	colon=user.index(":")
	gid=100
	grp="users"

	if colon < 0:
		if grp in grps:
			grps[grp] = grps[grp] + "," + user
		else:
			grps[grp] = user
	else:
		grp = user[colon+1:]
		user = user[:colon]
		gs = grp.split(",")
		if len(gs) > 0:
			for g in gs:
				if g in grps:
					grps[g] = grps[g] + "," + user
				else:
					grps[g] = user
				if not g in grp_ids:
					grp_ids[g]=uid
			grp=gs[0]
		else:
			grp_ids[grp]=uid

	gid=grp_ids[grp]

	if r[0] == "-":
		home="/tmp"
		shell="/sbin/false"
	else:
		home="/ram/home/" + user
		shell="/sbin/sh"
		print (user+":"+r[0]+":16750:0:::::",file=sfd)
		os.makedirs(home,exist_ok=True)
		os.chown(home,int(uid),int(gid))
		make_auth_keys.user(user,int(uid),int(gid))
		shutil.copy2("/etc/user_profile",home+"/.profile")

	print(user+":x:"+str(uid)+":"+str(gid)+"::"+home+":"+shell,file=pfd)


sfd.close()
pfd.close()


with open("/ram/etc/group","w") as gfd:
	print("root:x:0:root",file=gfd)
	print("nobody:x:9999:nobody",file=gfd)
	for g in grps:
		print(g+":x:"+str(grp_ids[g])+":"+grps[g],file=gfd)


rrr=stat.S_IRUSR+stat.S_IRGRP+stat.S_IROTH

os.chmod("/etc/shadow",stat.S_IRUSR)
os.chmod("/etc/passwd",rrr)
os.chmod("/etc/group",rrr)

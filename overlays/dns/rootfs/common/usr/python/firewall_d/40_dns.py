#! /sbin/python
#
# (c) Copyright 2017-2018 James Stevens (james@jrcs.net) - All Rights Reserved
# see License.txt for details

import __opts__,opts, slimlib
import __firewall__


def fn_40_dns(ipv):
	dns_local="1024:65535"

	print("-A INPUT -p udp -m udp --dport 53 -j UDPDNS")
	print("-A INPUT -p tcp -m tcp --dport 53 -j TCPDNS")
	print("-A OUTPUT -p udp -m udp --sport 53 -j OUTUDPDNS")
	print("-A OUTPUT -p tcp -m tcp --sport 53 -j OUTTCPDNS")

	if slimlib.opt_is_y("dnsResolver"):
		print("-A INPUT -p udp --dport "+dns_local+" --sport 53 -j ACCEPT")
		print("-A INPUT -p tcp --dport "+dns_local+" --sport 53 -j ACCEPT")
		print("-A OUTPUT -p udp --sport "+dns_local+" --dport 53 -j ACCEPT")
		print("-A OUTPUT -p tcp --sport "+dns_local+" --dport 53 -j ACCEPT")
	else:
		add_external_resolvers(ipv)
		
		
	if "dnsRndcKey" in __opts__.opt_vals:
		if "dnsRndcAllow" in __opts__.opt_vals:
			for all in slimlib.by_addr_type(__opts__.opt_vals["dnsRndcAllow"],ipv):
				print("-A INPUT -p tcp -s "+all+" --dport 953 -j ACCEPT")
				print("-A OUTPUT -p tcp -d "+all+" --sport 953 -j ACCEPT")
		else:
			print("-A INPUT -p tcp --dport 953 -j ACCEPT")
			print("-A OUTPUT -p tcp --sport 953 -j ACCEPT")


	if slimlib.opt_is_y("dnsWithSecondary"):
		with open(__opts__.syscfg,"r") as sysfd:
			lines = [ l.strip()[14:].strip('"').strip("'") for l in sysfd if l.startswith("dnsSecondary=") ]
			for l in lines:
				if l.find(" ") < 0: continue
				l = l[l.find(" "):]
				while l[0]==" ": l=l[1:]
				for all in slimlib.by_addr_type(l,ipv):
					print("-A UDPDNS -s",all," -j ACCEPT")


	loc="1b"
	if ipv == "6": loc="3d"

	if slimlib.opt_is_y("firewallBlockResp"):
		if slimlib.opt_is_y("firewallLogging"):
			print("-A UDPDNS -m u32 --u32 0x"+loc+"&0x80=0x80 -j LOG --log-prefix <RESP>")
		print("-A UDPDNS -m u32 --u32 0x"+loc+"&0x80=0x80 -j DROP")


	if ("firewallBlockRD1" in __opts__.opt_vals 
		and not __opts__.opt_vals["firewallBlockRD1"] == "N" 
		):
		for all in slimlib.by_addr_type(__opts__.opt_vals["dnsResolverAllowed"],ipv):
			print("-A RD1 -s "+all+" -j RETURN")

			if not slimlib.opt_is_y("firewallBlockRD1"):
				x = __opts__.opt_vals["firewallBlockRD1"]
				if x.isdigit():
					l = int(x)
					if l <= 0: l=10
				else:
					l=10

				b = l / 10
				if b <= 5: b=5

				print("-A RD1 -m limit --limit "+str(l)+" --limit-burst "+str(b)+" -j RETURN")
				
				if slimlib.opt_is_y("firewallLogging"):
					print("-A RD1 -j LOG --log-prefix <RD1>")

		print("-A RD1 -j DROP")
		print("-A UDPDNS -m u32 --u32 0x"+loc+"&0x1=1 -j RD1")

	print("-A OUTUDPDNS -j ACCEPT")
	print("-A OUTTCPDNS -j ACCEPT")
	print("-A UDPDNS -j ACCEPT")
	print("-A TCPDNS -j ACCEPT")


__firewall__.fw_fns.append(fn_40_dns)

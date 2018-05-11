#!/bin/python3

import subprocess
import os
import re
import sys
import json
from jinja2 import Environment, FileSystemLoader

## This program is used to setup a network namespace with a wiregurad peer running inside, for trafic redirection

def do_make_nns(nns, nameserver=None):
	mk = ["ip", "netns", "add",  nns]
	setup = nns_wrap(nns, link_up("lo"))
	subprocess.call(mk)
	subprocess.call(setup)
	if not nameserver is None:
		directory = "/etc/netns/" + nns
		if not os.path.exists(directory):
			os.makedirs(directory)
		dnsf = open(directory + "/resolv.conf", "w")
		dnsf.write("nameserver %s" % nameserver)
		dnsf.close()

def delete_nns(nns):
	subprocess.call(["ip", "netns", "delete", nns])

def do_add_peers(nns, ip4_setup=None, ip6_setup=None, use_direct_table=False):
	#variables
	veth = nns + "-veth"
	peer = nns + "-peer"
	#setup links
	subprocess.call(["ip", "link", "add", veth, "type", "veth", "peer", "name", peer])
	subprocess.call(move_link(peer, nns))
	subprocess.call(nns_wrap(nns, link_up(peer)))
	subprocess.call(link_up(veth))

	#setup ipv4 routing
	if not ip4_setup is None:
		addr_veth = ip4_setup["addr"]
		snmask = ip4_setup["mask"]
		addr_peers = ip4_setup["peers"]
		#add addresses
		subprocess.call(link_addr(veth, addr_veth + ("/%d" %  snmask)))
		for peer_addr in addr_peers:
			subprocess.call(nns_wrap(nns, link_addr(peer, peer_addr + ("/%d" %  snmask))))
		#add routes
		subprocess.call(nns_wrap(nns, route_add(peer, addr_veth, "main", snmask, True)))
		if use_direct_table:
			subprocess.call(route_add(veth, addr_veth, "direct", snmask))

	#setup ipv6 routing
	if not ip6_setup is None:
		addr6_veth = ip6_setup["addr"]
		addr6_peers = ip6_setup["peers"]
		snmask = ip6_setup["mask"]
		#add addresses
		subprocess.call(link_addr(veth, addr6_veth + ( "/%d" % snmask), True))
		for peer_addr6 in addr6_peers:
			subprocess.call(nns_wrap(nns, link_addr(peer, peer_addr6 + ( "/%d" % snmask), True)))
			subprocess.call(["ip", "-6", "neigh", "add", "proxy", peer_addr6, "dev", veth])
		#add routes
		subprocess.call(nns_wrap(nns, route_add(peer, addr6_veth, "main", snmask, True, True)))
		if use_direct_table:
			subprocess.call(route_add(veth, addr6_veth, "direct", snmask, False, True))
	

def nns_wrap(nns ,cmd):
	c = ["ip", "netns", "exec", nns]
	return c + cmd

def link_up(link):
	c = ["ip", "link", "set", link, "up"]
	return c

def link_addr(link, addr, ipv6=False):
	if not ipv6:
		c = ["ip", "addr", "add", addr, "dev", link]
	else:
		c = ["ip", "-6", "addr", "add", addr, "dev", link]
	return c

def move_link(link, nns):
	c = ["ip", "link", "set", link, "netns", nns]
	return c

def route_add(link, addr, table, net, default=False, ipv6=False):
	c = [ "ip" ]
	if ipv6:
		c.append("-6")
	if default:
		c += [ "route", "add", "default", "via", addr, "dev", link, "table", table]
	else:
		c += [ "route", "add", addr + "/%d"%net , "dev", link, "table", table]
	return c

def main():
	if len(sys.argv) < 3:
		print("Usage: %s [start|stop] [netnsconf.json]" % sys.argv[0])
		return
	f = open(sys.argv[2])
	nns_config = json.load(f)

	nns = nns_config["name"]
	dns = nns_config["dns"]
	use_direct=nns_config["use_direct_rt"]
	ip4 = nns_config["ip4"]
	ip6 = nns_config["ip6"]

	#if start setup nns
	if sys.argv[1] == "start":
		do_make_nns(nns, dns)
		do_add_peers(nns, ip4, ip6, use_direct)

	# delete nns
	else:
		delete_nns(nns)

if __name__ == "__main__":
	main()

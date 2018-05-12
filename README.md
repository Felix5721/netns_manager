NetnsManager
============

Netnsmanager is a small python program that setup up an linux network namespace with a one peer that can be assigned multiple ips. It supports ipv4 and ipv6 addressen.

# Usage

## Direct 

You need to be root in order for this program to work:

> netnsmanager start/stop netnsconf.json 

This will create a network namespace based on the setting in the specified json file. An example json file can be found in the netns foulder. 

## Systemd

> systemctl start netnsmanager@<name>

Use systemd to launch netnsmanger with the json file located at /etc/netns_manager/netns/<name>.json

# Installation

run ./install.sh as root


#!/bin/bash

if [[ $UID != 0 ]]; then
  echo "This must be run as root."
  exit 1
fi

mv netnsmanager.py /usr/bin/netnsmanager
mkdir -p /etc/netns_manager
cp -rf netns	/etc/netns_manager
cp -f systemd/netnsmanager@.service /etc/systemd/system/

echo "Installion Done"

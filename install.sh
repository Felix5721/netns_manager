#!/bin/bash

if [[ $UID != 0 ]]; then
  echo "This must be run as root."
  exit 1
fi

go build netnsmanager.go
mv netnsmanager /usr/bin
mkdir -p /etc/netns_manager
cp -rf scripts /etc/netns_manager
cp -rf netns	/etc/netns_manager
cp -f systemd/netnsmanager@.service /etc/systemd/system/

echo "Installion Done"

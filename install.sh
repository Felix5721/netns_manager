#!/bin/bash

if [[ $UID != 0 ]]; then
  echo "This must be run as root."
  exit 1
fi

go build netnsmanager.go
mv netnsmanager /usr/bin
mkdir -p /etc/netns_manager
cp -r scripts /etc/netns_manager
cp -r netns	/etc/netns_manager
cp systemd/netnsmanager@.service /etc/systemd/system/

echo "Installion Done"

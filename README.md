# NetnsManager
Go Program to start different network namespaces at boot

To get this working run:

go build netnsmanager.go

This will create an executable named netnsmanager.
To use it call as root:

./netnsmanager start/stop netnsconf.json 

this will create or delete a network namespace based on the settings set in the json file 

To make this command availble from outside the directory do the following.

create the directory /etc/netns_manager

then copy the scripts directory to it

move the netnsmanager executable to a directory which is in your PATH

to use netnsmanager with systemd create a netns directory in /etc/netns_manager here you will put all json config files

copy the systemd service file to /etc/systemd/system, now you can start the service:

systemctl start netnsmanager@sample

this will create a network namespace with the configfile /etc/netns_manager/netns/sample.json

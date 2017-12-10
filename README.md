# NetnsManager
Go Program to start different network namespaces at boot

To get this working run:

go build netnsmanager.go

this will create an executable named netnsmanager
To use it call:

./netnsmanager start/stop netnsconf.json 

this will create or delete a network namespace based on the settings set in the json file 

To make this command availble from outside the directory do the following.

create the directory /etc/netns_manager
then copy the scripts directory to it
move the netnsmanager executable to a directory which is in your PATH

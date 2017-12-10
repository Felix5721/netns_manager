#!/bin/bash

if [[ $UID != 0 ]]; then
  echo "This must be run as root."
  exit 1
fi

function setup_ns(){
  ns_name=$1
  ns_peer=$ns_name-peer
  ns_veth=$ns_name-veth
  ipveth=$2
  ippeer=$3
  mask=$4
  

  #Create Namespace and set up loopback
  ip netns add $ns_name
  ip netns exec $ns_name ip link set lo up

  #create veth and peer
  ip link add $ns_veth type veth peer name $ns_peer

  #add peer to namespace
  ip link set $ns_peer netns $ns_name

  #setup addresses for veth and peer
  ip addr add $ipveth/$mask dev $ns_veth
  ip netns exec $ns_name ip addr add $ippeer/$mask dev $ns_peer
  ip link set $ns_veth up
  ip netns exec $ns_name ip link set $ns_peer up

  #set default route for namespace
  ip netns exec $ns_name ip route add default dev $ns_peer
}

setup_ns $1 $2 $3 $4

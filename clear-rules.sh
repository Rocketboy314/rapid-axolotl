#!/bin/bash

echo clearing rules!

# CLEAR RULES
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

echo reseting default policies for input, output, and forward chains!

# RESET DEFAULT POLICIES
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT

echo attempting to kill portspoof, if running!

killall portspoof
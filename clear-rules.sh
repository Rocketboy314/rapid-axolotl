#!/bin/bash

echo clearing rules!

# CLEAR RULES
iptables -F
iptables -X
iptables -t nat -F
iptables -t mangle -F

echo reseting default policies for input, output, and forward chains!
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT
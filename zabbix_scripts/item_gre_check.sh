#!/bin/bash
#
# gre monitor
# ping dstip; loss 100%[1] or not 100%[0]
# 1: NO
# 0: OK

dstip=$1
loss=`ping -w2 -c2 ${dstip} | awk '{gsub(/%/,"",$0);if($0~/packet loss/)print $6}'`
echo ${loss}

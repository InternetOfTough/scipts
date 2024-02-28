#!/bin/sh

max=2000
for i in `seq 1 $max`
do
	time=$(date '+%D +%T')
	echo "$time"
	signal=$(/sbin/iwconfig  wlan0 | grep -i Link )
	echo "$signal"
	sleep 1
done

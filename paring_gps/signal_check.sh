#!/bin/sh

max=2000
for i in `seq 1 $max`
do
	time=$(date '+%D +%T')
	echo "$time"
	sleep 1
	iwconfig wlan0 | grep -i Link
done

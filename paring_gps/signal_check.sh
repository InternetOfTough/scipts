#!/bin/sh

max=2000
for i in `seq 1 $max`
do
	#time=$(date '+%s')
	echo "$i"
	#echo 'sum = $a'
	sleep 1
	#iw=$(sudo iwconfig wlan0)
	#iw=$(  iwconfig wlan0 | awk -F'[ :=]+' '/Freq/{gsub("\\.","");f=$5}/Signal/{s=$7}END{print s","f}')
	#echo $iw
	iwconfig
done

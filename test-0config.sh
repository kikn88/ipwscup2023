#!/bin/bash

Team=00		# my team ID
Target=00	# target team ID
python=python3
Csv=Csv
A=$Csv/A.csv
B=$Csv/B${Team}.csv
C=$Csv/C${Team}.csv
X=$Csv/X${Team}.csv
D=$Csv/D${Team}.csv
E=$Csv/E${Target}by${Team}.csv

pytest(){
	echo $*
	$python  $* 
}








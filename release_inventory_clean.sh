#!/bin/bash
#Date:
#Author:
#Task:


path="./releases"
recent_versions=3
days_ago=$(date -d 'now - 30 days' +%s)

keep_current_latest_version()
{

	cd $path
	if [ `ls -d ver*|wc -l` -lt $recent_versions ];
	then
		echo "Not enough release files, No need to clean"
	fi
	## get current file and symbolic
	current_version_ln=`ls |grep current`
	current_version=`readlink -f current|awk -F '/' '{print $6}'`

	## get all version  expect current list
	recent_version_number=''
	for i in `ls |grep ver|grep -v $current_version|grep -v $current_version_ln`
        do
                recent_version_number=${i:3:${#i}-3}" "$recent_version_number
        done
	echo $recent_version_number

	release_file_seq=0

	for i in $recent_version_number
	do
		## skip recent version files, recent is defined by seq of version
		if [ $release_file_seq -lt $recent_versions ];
		then
			release_file_seq=$((release_file_seq+1))
			continue
		else
			if [ $(date -r "ver""$i" +%s) -lt $days_ago ];
			then
				echo "rm -rf ""ver""$i"
				rm -rf "ver""$i"
			fi
		fi
	done
}



keep_current_latest_version

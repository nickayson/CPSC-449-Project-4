#!/bin/sh

# printing out locations related to rq that cron will use 
curr_loc=$(pwd)
echo "location of rq_enqueue.sh: ${curr_loc}/bin"
echo "location of rq_enqueue_log.txt: ${curr_loc}/var/rq_log"

# output the string to be put in crontab
echo "\nTo add this task to cron, open crontab with command \n              crontab -e"
echo "Below is the string you need to add: "
echo "*/10 * * * * bash -l ${curr_loc}/bin/rq_enqueue.sh >> ${loc_loc}/var/rq_log/rq_enqueue_log.txt 2>&1"

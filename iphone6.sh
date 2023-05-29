#!/usr/bin/bash
n=$(/usr/bin/python3 update_cron_parameter.py)
echo $n
if [ $n -ge 1 -a $n -le 48 ]
then
`/usr/bin/python3 sample_search.py $n`
fi
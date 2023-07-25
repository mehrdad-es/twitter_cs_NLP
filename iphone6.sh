#!/usr/bin/bash
for ((i=1; i<=36; i++))
do
n=$(./venv/bin/python3 update_cron_parameter.py)
echo $n
if [ $n -ge 1 -a $n -le 36 ]
then
`./venv/bin/python3 sample_search.py $n`
fi
done
`aws s3 sync s3://tw-storage-2023/train-etl-iphone ./bucket --quiet`
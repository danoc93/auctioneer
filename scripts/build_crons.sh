dir=$(pwd)
echo "PATH=/usr/local/bin:/usr/local/sbin:~/bin:/usr/bin:/bin:/usr/sbin:/sbin"
echo "* * * * * cd $dir && pipenv run $dir/manage.py complete_bids  >> /tmp/logs/complete_bids.log 2>&1"

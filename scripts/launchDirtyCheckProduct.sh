#!/bin/bash
yesDay=`date -d yesterday +%Y/%m/%d`
yesMonth=`date -d yesterday +%Y/%m`
echo $yesDay
echo $yesMonth
#1.first step is to get the yesterday hdfs data to local dir
hdfsOpenDataPath='/jjbox/open/'$yesDay
hdfsCloseDataPath='/jjbox/close/'$yesDay
hdfsUsbDataPath='/jjbox/usb/'$yesDay

echo $hdfsOpenDataPath
echo $hdfsCloseDataPath
echo $hdfsUsbDataPath


localOpenDataPath='/data/application/dongliang/hdfs/open/'$yesMonth
localCloseDataPath='/data/application/dongliang/hdfs/close/'$yesMonth
localUsbDataPath='/data/application/dongliang/hdfs/usb/'$yesMonth

echo $localOpenDataPath
echo $localCloseDataPath
echo $localUsbDataPath
hadoop fs -test -e $hdfsOpenDataPath
if [ $? -eq 0 ] ;then
	echo 'hdfs open data of yesterday exists'
	hadoop fs -get $hdfsOpenDataPath $localOpenDataPath
	if [ $? == 0 ]
	then
        	echo 'execute hadoop get open data success'
	else
        	echo 'execute hadoop get open data failed'
	fi
else
	echo 'open data of yesterday not exists'
fi

hadoop fs -test -e $hdfsCloseDataPath
if [ $? == 0 ] ;then
	echo 'hdfs close data of yesterday exists'
	hadoop fs -get $hdfsCloseDataPath $localCloseDataPath
        if [ $? == 0 ]
        then
                echo 'execute hadoop get close data success'
        else
                echo 'execute hadoop get close data failed'
        fi
else
	echo 'close data of yesterday not exists'
fi

hadoop fs -test -e $hdfsUsbDataPath
if [ $? == 0 ] ;then
	echo 'hdfs usb data of yesterday exists'
	hadoop fs -get $hdfsUsbDataPath $localUsbDataPath
        if [ $? == 0 ]
        then
                echo 'execute hadoop get usb data success'
        else
                echo 'execute hadoop get usb data failed'
        fi
else
	echo 'usb data of yesterday not exists'
fi

#2.second step is to call the python check dirty data scripts
python /data/application/dongliang/dataCheckScripts/checkOpenDirtyDataEveryDay.py
python /data/application/dongliang/dataCheckScripts/checkCloseDirtyDataEveryDay.py
python /data/application/dongliang/dataCheckScripts/checkUsbDirtyDataEveryDay.py

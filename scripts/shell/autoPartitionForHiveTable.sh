#!/bin/bash

#this scripts is for auto create hive external table which location to the open,close,usb hdfs dir for yesterday
#and add hour partition to the dir,then get all the fields of the external table and finally insert
#into the normal table

hive -e '
use ods;
create external table if not exists original_device_open
(
opencontent string
) 
PARTITIONED BY (year string, month string, day string,hour string)
row format delimited 
fields terminated by "\t"
lines terminated by "\n" 
stored as textfile
location  "/jjbox/open";exit;'

echo 'create device open table successfully'
yesdaypart=`date +%Y/%m/%d -d '-1 day'`
year=`echo $yesdaypart | cut -d \/ -f 1`
month=`echo $yesdaypart | cut -d \/ -f 2`
day=`echo $yesdaypart | cut -d \/ -f 3`
echo "yesterday date is:"$yesdaypart

#add hive partition for yesterday hours
i=0
max=24

while [ $i -lt $max ]
do
  if [ ${#i} == 1 ]
  then
      hour=`printf %02d $i`
      echo "the hour<10 is---"$hour
  elif [ ${#i} == 2 ]
  then
      hour=$i
  fi
  hours[$i]=$hour
  echo "the element in hours is----"${hours[$i]}
  let i+=1
done

element_count=${#hours[@]}
echo "element_count is---"$element_count
index=0
while [ $index -lt $element_count ]
do
  hourstr=${hours[$index]}
  hql="use ods;ALTER TABLE original_device_open ADD PARTITION(year=${year},month=${month},day=${day},hour=${hourstr}) LOCATION '/jjbox/open/${yesdaypart}/${hourstr}';exit;"
  echo "the hql is----"$hql
  hive -e "$hql"
  let index+=1
done

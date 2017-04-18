#!/usr/bin/python
import json
import datetime
import time
import os
import os.path


def check_time_field(path, field):
    f = open(path, 'r')
    for line in f:
        # jsonstr = json.dumps(line)
        content = json.loads(line)
        timefield = content[field]
        print 'the time field is:', timefield
        cmpresult = compare_time('2017-01-03', timefield[0:10])
        if (cmpresult > 0):
            print 'the line contains error date is:', line
        else:
            print 'the noraml line is:', line


def day_get(d, interval):
    oneday = datetime.timedelta(days=interval)
    day = d - oneday
    return day.strftime('%Y/%m/%d')


def scan_offline_hdfsfiles(rootdir):
    if (os.path.exists(rootdir)):
        list = os.listdir(rootdir)
        for i in range(0, len(list)):
            path = os.path.join(rootdir, list[i])
            if os.path.isfile(path):
                print 'here is the file path:', path
            else:
                sublist = os.listdir(path)
                for j in range(0, len(sublist)):
                    subfilepath = os.path.join(path, sublist[j])
                    print 'the offline hdfs path is:', subfilepath
                    opentimefield = check_time_field(subfilepath, 'opentime')
    else:
        print "the hdfs dir does not exists"


def compare_time(time1, time2):
    s_time = time.mktime(time.strptime(time1, '%Y-%m-%d'))
    e_time = time.mktime(time.strptime(time2, '%Y-%m-%d'))
    print 's_time is:', s_time
    print 'e_time is:', e_time
    return int(s_time) - int(e_time)


hdfsfilepathprefix = '/var/lib/hadoop-hdfs/testFiles/hdfs/jjbox/open/'
d = datetime.datetime.now()
hdfsdaydir = hdfsfilepathprefix + day_get(d, 7)
print 'the scan hdfs dir is:', hdfsdaydir
scan_offline_hdfsfiles(hdfsdaydir)

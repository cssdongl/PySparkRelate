#!/usr/bin/python
import json
import datetime
import time
import os
import os.path

logPath = '/data/application/dongliang/dataCheckScripts/checkLogs/closeDataCheck.log'
def check_time_field(path,field):
    f = open(path, 'r')
    logFile = open(logPath,'a+')
    for line in f:
        content = json.loads(line)
	timefield = content[field]
        cmpresult = compare_date('2017-01-03',timefield[0:10])
	if(cmpresult>0):
	    print 'the line contains error date<2017-01-03 is:\n'
	    logFile.write(line+'\n')
    f.close()
    logFile.close()

def check_two_time_field(path,field1,field2):
    f = open(path, 'r')
    logFile = open(logPath,'a+')
    for line in f:
        content = json.loads(line)
        opentimefield = content[field1]
	closetimefield = content[field2]
        print 'the open time field is:',opentimefield
	print 'the close time field is:',closetimefield
        cmpresult = compare_time(opentimefield,closetimefield)
        if(cmpresult>0):
            print 'the line of closetime > opentime is:\n'
	    logFile.write(line+'\n')
    f.close()
    logFile.close()
    
def day_get(d,interval):
    oneday = datetime.timedelta(days=interval)
    day =d - oneday
    return day.strftime('%Y/%m/%d')

def scan_offline_hdfsfiles(rootdir):
    if(os.path.exists(rootdir)):
        list = os.listdir(rootdir)
        for i in range(0,len(list)):
	    path = os.path.join(rootdir,list[i])
	    if os.path.isfile(path):
	        print 'here is the file path:',path
	    else:
	       sublist = os.listdir(path)
	       for j in range(0,len(sublist)):
                   subfilepath = os.path.join(path,sublist[j])
                   print 'the local close data file path is:',subfilepath
		   check_two_time_field(subfilepath,'opentime','closetime')
	           check_time_field(subfilepath,'opentime')
    else:
	print "the local close data dir does not exists"

def compare_time(time1,time2):
    s_time = time.mktime(time.strptime(time1,'%Y-%m-%d %H:%M:%S'))
    e_time = time.mktime(time.strptime(time2,'%Y-%m-%d %H:%M:%S'))
    return int(s_time) - int(e_time)

def compare_date(time1,time2):
    s_time = time.mktime(time.strptime(time1,'%Y-%m-%d'))
    e_time = time.mktime(time.strptime(time2,'%Y-%m-%d'))
    return int(s_time) - int(e_time)
    

hdfsfilepathprefix= '/data/application/dongliang/hdfs/close/'
d = datetime.datetime.now()
hdfsdaydir = hdfsfilepathprefix + day_get(d,1)
print 'the scan local close data dir is:',hdfsdaydir
scan_offline_hdfsfiles(hdfsdaydir)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import time
import os

pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}) - - (\[.*\]) (".*") (\d{3}) (\d+)'
logfilepath = 'localhost_access_log.2014-07-19.txt'
recordpath = 'record.log'
p = re.compile(pattern)
accessURLSummary = {}
summary = 0
filelineno = 0
fileSeek = 0

def logParse():
    """日志分析统计"""
    global summary
    global filelineno
    global accessURLSummary
    global fileSeek
    with open(logfilepath) as filehandler:
        filehandler.seek(fileSeek)
        for Line in filehandler:
            findLineList = p.findall(Line)
            for findLine in findLineList:
                if findLine[2] in accessURLSummary:
                    accessURLSummary[findLine[2]] += 1
                else:
                    accessURLSummary[findLine[2]] = 1
            filelineno += 1
        fileSeek = filehandler.tell()

def writeRecord():
    """使用文件recordpath来保存上一次执行的信息"""
    with open(recordpath,'w') as filehandler:
        filehandler.write(str(fileSeek)+'\n')
        filehandler.writelines([item + "###" + str(accessURLSummary[item]) + '\n' for item in accessURLSummary])

def readRecord():
    """读取文件recordpath获取相对应的信息"""
    global accessURLSummary
    global fileSeek
    if os.path.exists(recordpath):
        with open(recordpath) as filehandler:
            lastSeekNumber = int(filehandler.readline())
            for line in filehandler:
                tempList = line.split('###')
                accessURLSummary[tempList[0]] = int(tempList[1])
        fileSeek = lastSeekNumber
    else:
        pass

def timeDict(baseTime):
    monthEnum = ('None','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
    return {'tm_year':str(baseTime.tm_year),
            'tm_mday':str(baseTime.tm_mday),
            'tm_mon':str(monthEnum[baseTime.tm_mon]),
            'tm_hour':str(baseTime.tm_hour),
            'tm_min':str(baseTime.tm_min),
            'tm_sec':str(baseTime.tm_sec)}

def findTimeRangePattern(start,end):
    start = "%(tm_mday)s/%(tm_mon)s/%(tm_year)s:%(tm_hour)s:%(tm_min)s:%(tm_sec)s" % timeDict(start)
    end = "%(tm_mday)s/%(tm_mon)s/%(tm_year)s:%(tm_hour)s:%(tm_min)s:%(tm_sec)s" % timeDict(end)
    findpattern = r"^.*\[%(start)s.*].* \[%(end)s.*].*\n" % {'start':start,'end':end}
    return findpattern

def locateRange(baseTime = time.time(), timeRange = 60):
    """确定搜索的范围"""
    biasTime = time.localtime(baseTime+timeRange)
    baseTime = time.localtime(baseTime)
    if timeRange < 0:
        start = biasTime
        end = baseTime
    else:
        start = baseTime
        end = biasTime
    timeRangePattern = findTimeRangePattern(start,end)
    print timeRangePattern
    with open(logfilepath) as filehandler:
        fReadLines = filehandler.readlines()
        print re.match(timeRangePattern, fReadLines)

def strToTime(timeStr):
    #monthEnum = {'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6','Jul':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}
    tempList = timeStr.split(':')
    tempDate = tempList[0].split('/')
    tm_Dict = {}
    tm_Dict['tm_mday'] = tempDate[0]
    tm_Dict['tm_mon']  = tempDate[1]
    tm_Dict['tm_year'] = tempDate[2]
    tm_Dict['tm_hour'] = tempList[1]
    tm_Dict['tm_min']  = tempList[2]
    tm_Dict['tm_sec']  = tempList[3]
    tm_str = "%(tm_mday)s/%(tm_mon)s/%(tm_year)s:%(tm_hour)s:%(tm_min)s:%(tm_sec)s" % tm_Dict
    return time.mktime(time.strptime(tm_str, "%d/%b/%Y:%H:%M:%S"))


locateRange(strToTime('19/Jul/2014:22:14:13'),60)

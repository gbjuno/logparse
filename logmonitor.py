#!/usr/bin/env python
# -*- coding:utf8 -*-

import re
import os
import time


def main():
    """
    主程序，用于调用各个函数流程
    """
    pattern = ''.join(['(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - ',
                       '\[(?P<datetime>[^ ]+) \+0800] "(?P<httpmethod>\w+) ',
                       '(?P<accesspath>[^ ]+) HTTP/(?P<httpprotocol>[^ ]+)" ' 
                       '(?P<httpstatus>\d{3}) (?P<httpsize>\d+)'])
    logfilename = 'localhost_access_log.2014-07-19.txt'
    #logparse(logfilename, 0, pattern)
    logparse(logfilename, 0, pattern, calBeginTime("19/Jul/2013:00:33:56"))
    #logparse(logfilename, 0, pattern, calBeginTime(125920000))

def logparse(logfilename, logfileseek=0, pattern='error', beginTime=time.localtime(0)):
    """
    日志分析
    """
    linecount = 0
    pattern = re.compile(pattern)
    logfileseek = logfileseek
    timevalid = 0
    #判断配置文件是否存在，如存在则读上次的偏移位置以及行号
    if os.path.exists('logmonitor.config'):
        with open('logmonitor.config', 'r') as f:
            logfileseek = int(f.readline().strip())
            linecount = int(f.readline().strip())

    #读取日志文件，找到在合格时间内的404错误的一行
    with open(logfilename, 'r') as logfilehandler:
        logfilehandler.seek(logfileseek)
        print 'begin from line %s' % (linecount+1)
        print 'begin from time %s' % time.strftime("%d/%b/%Y:%H:%M:%S", beginTime)
        for line in logfilehandler:
            linecount += 1
            itemDict = pattern.match(line)
            if time.strptime(itemDict.group('datetime'), "%d/%b/%Y:%H:%M:%S") > beginTime:
                if not timevalid:
                    print "valid time line number start from %s" % linecount
                    timevalid += 1
                if itemDict.group('httpstatus') == '404':
                    print "line number is %s ,error occur" % linecount
        filePositionRecord = logfilehandler.tell()               
    
    #将偏移位置以及行号写入配置文件，留待下一次使用
    with open('logmonitor.config', 'w') as configfilehandler:
        configfilehandler.writelines([str(filePositionRecord)+'\n',str(linecount)])

def calBeginTime(timerange):
    """
    根据当前时间和时间间隔，获得最终的起始时间
    """
    if isinstance(timerange, int):
        now = time.time()
        beginTime = time.localtime(now-timerange)
    else:
        beginTime = time.strptime(timerange, "%d/%b/%Y:%H:%M:%S")
    return beginTime

if __name__ == '__main__':
    main()

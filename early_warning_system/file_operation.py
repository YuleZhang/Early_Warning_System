# -- coding: utf-8

import time
import os

def TimeStampToTime(timestamp):
    # 把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

def get_FileSize(filePath):
    # 获取文件大小，结果保留两位小鼠，单位为mb
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024*1024)
    return round(fsize,2)

def get_FileCreateTime(filePath):
    # 获取文件的创建时间
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)
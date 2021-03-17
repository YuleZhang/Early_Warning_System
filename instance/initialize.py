# -*- coding= utf-8 -*-
'''
主要进行最初的初始化操作，包括数据库基本表格初始化
以及文件初始状态的设置
'''
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)+'/'+'..'))
from early_warning_system.database import DatabaseOperations
from early_warning_system.file_operation import get_FileCreateTime,get_FileSize
sql_path = 'db.sql'
data_path = '../data'
db = DatabaseOperations()

def init_tables():
    fd = open(sql_path,'r',encoding='utf-8')
    sqlFile = fd.read()
    sqlCommands = sqlFile.split(';')
    db.init_by_sql(sqlCommands)
    fd.close()
    print('数据库表格初始化成功')

def init_files():
    # 初始化目录文件列表
    path = os.path.abspath(__file__) #文件位置
    current_path = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")  #当前目录 
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".") #父目录
    db = DatabaseOperations()
    catalog = os.listdir(data_path)
    summary = []
    for f in catalog:
        file_path = os.path.join(data_path,f)
        abs_path = os.path.join(father_path,'data',f)
        size = get_FileSize(file_path)
        create_time = get_FileCreateTime(file_path)
        summary.append(tuple([f,size,create_time,abs_path]))
    db.insert_history(summary)
    print('data目录初始化成功')

if __name__ == "__main__":
    init_tables()
    init_files()
    
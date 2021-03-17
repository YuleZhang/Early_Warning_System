#-*- encoding= utf-8 -*-
import traceback
import pymysql

# try except装饰器
def catch_error(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
            print('success operation')
        except Exception as e:
            print('operation error',e)
    return wrapper

class DatabaseOperations():
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.conn = pymysql.connect(host=self.host,user=self.user,password=self.password)
        self.cursor = self.conn.cursor()
        self.conn.select_db('EWS')

    @catch_error
    def init_by_sql(self,sql_commands):
        for command in sql_commands:
            if command == '': continue
            self.cursor.execute(command)

    @catch_error
    def insert_history(self,result):
        sql = "insert into file_history value(NULL,%s,%s,%s,%s)"
        self.cursor.executemany(sql,result)

    @catch_error
    def delete_file_history(self,fileID):
        sql = "delete from file_history where HistID = '"+fileID+"'"
        self.cursor.execute(sql)
        self.conn.commit()

    @catch_error
    def search_file_history(self):
        sql = 'select * from file_history'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    @catch_error
    def search_rules_history(self):
        sql = 'select * from rule_history'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    @catch_error
    def insert_rules_history(self,rules):
        sql = "insert into rule_history value(NULL,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.executemany(sql,rules) 

    # 批量插入课程字典表极大的提高效率
    @catch_error
    def insert_course(self,result): 
        # 注意result为元组列表，加入ignore能够忽略插入重复数据的错误
        sql = "insert ignore into CourseNum(CNNum,CNName,CNCredit,CNHour,CNAttribute) value(%s,%s,%s,%s,%s)"
        self.cursor.executemany(sql,result)

    # 向学生成绩表添加数据
    @catch_error
    def insert_student_grade(self,result):
        sql = "insert ignore into student_grade(SGID,SGName,SGLevel,SGClass,SGCourseNum,SGCourseGrade) value(%s,%s,%s,%s,%s,%s)"
        self.cursor.executemany(sql,result)

    # 联合查询
    @catch_error
    def search_student_grade(self):
        sql =  "select * from student_grade"
        # sql = "select SGID,SGName,SGLevel,SGClass,SGCourseNum,SGCourseGrade,CNName,CNAttribute from student_grade s left join coursenum c on s.SGCourseNum = c.CNNum"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
    
    # 查询字典表
    @catch_error
    def search_course(self,course_num):
        sql = "select * from CourseNum where CNNum = '" + course_num +"'"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
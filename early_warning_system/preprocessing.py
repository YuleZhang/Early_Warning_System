# -*- encoding: utf-8 -*-

from early_warning_system.database import DatabaseOperations
from early_warning_system.apriori import Apriori
import numpy as np
import pandas as pd
import datetime
import os

def read_all_xlsx(path):
    # 从指定路径下读取xlsx表后合并
    db = DatabaseOperations()
    histories = db.search_file_history()
    # catalog = os.listdir(path)
    summary = []
    for f in histories:
        file_path = f[4]
        print("正在读取文件: ",f[4])
        summary.append(pd.read_excel(file_path,header=0))
    df = pd.concat(summary)
    return df

def read_single_xlsx(path):
    # 从指定路径下读取xlsx表后合并
    summary = []
    print("正在读取文件: ",path)
    summary.append(pd.read_excel(path,header=0))
    df = pd.concat(summary)
    return df

def course_preprocess(df):
    # 对原始数据进行预处理，并存入导数据库中
    df.columns = df.columns.str.strip()
    df.drop_duplicates(subset=None, keep='first', inplace=True)
    df = df.astype(object).where(pd.notnull(df), None)
    # df.dropna(axis = 0,inplace=True)
    undupNum = np.array(list(set(df['课程号'].values.tolist())))
    course = []
    stu_grade_tb = []
    high_freq = []
    # 获取高频课程
    for num in undupNum:
        course_info = df[df['课程号']==num]
        course_name = course_info['课程名'].tolist()[0]
        if course_info.shape[0] > 100:
            high_freq.append(num)
        
    # 遍历不重复的高频课程号
    for num in high_freq:
        if num is None or len(num)==0 or num == "nan":continue
        hour = -1
        course_info = df[df['课程号']==num]
        cRows = course_info.shape[0] # 获得行数
        if cRows < 3: continue # 过滤稀疏课程数据，提高计算效率
        course_name = course_info['课程名'].tolist()[0]
        credit = course_info['学分'].tolist()[0]
        if '学时' in df.columns.tolist():
            hour = course_info['学时'].tolist()[0]
        attribute = course_info['选课属性'].tolist()[0]
        course.append(tuple([num,course_name,credit,hour,attribute]))
    # 遍历每一行成绩数据
    for index,row in df.iterrows():
        if row['成绩'] is None or row['课程号'] not in high_freq: continue
        stu_id = row['学号']
        stu_name = row['姓名']
        stu_level = row['年级']
        stu_class = row['班级']
        stu_course = row['课程号']
        stu_grade = get_grade_label(row['成绩'].strip())
        stu_grade_tb.append(tuple([stu_id,stu_name,stu_level,stu_class,stu_course,stu_grade]))
    dbop = DatabaseOperations()
    dbop.insert_course(course)
    dbop.insert_student_grade(stu_grade_tb)

def get_grade_label(grade):
    # 获取成绩对应标签
    if(type(grade) == int or (grade[0] > '0' and grade[0] < '9')):
        g = int(float(grade))
        if g >= 85: return "优"
        elif g >=75 and g < 85: return "良"
        elif g >= 60 and g < 75: return "中"
        elif g < 60: return "差"
    elif grade == "及格" or grade == "通过": return "中"
    elif grade == "不通过" or grade == "不及格": return "差"
    else: return "差"

def main(path,flag):
    course_df = []
    # if flag:
    course_df = read_all_xlsx(path)
    # else:
    # course_df = read_single_xlsx(path)
    print(course_df.head())
    course_preprocess(course_df)
    buildRules(0.3,0.6)

def load_data(level):
    db = DatabaseOperations()
    res = db.search_student_grade()
    df = pd.DataFrame(list(res),columns=['学号','姓名','年级','班级','课程号','成绩'])
    df = df[((df['年级']=='2015') & (df['成绩']==level))].head(1000)
    all_student_sum = []
    for name,group in df.groupby('学号'):
        s = [item['课程号']+'-'+item['成绩'] for idx,item in group.iterrows()]
        if len(s) > 1:
            all_student_sum.append(s)
    return all_student_sum

def buildRules(support,confidence):
    level = ['良','差','中','优']
    apr = Apriori()
    db = DatabaseOperations()
    cur_time = str(datetime.date.today())
    ans = []
    for item in level:
        data = load_data(item)
        L,supportData = apr.apriori(data,minSupport=support)
        rules=apr.generateRules(L,supportData,minConf=confidence)
        rules=list(rules)
        i = 0
        # sort the convidence about rules and print top 3 rules
        sorted_rules = sorted(rules, key = lambda x:float(x[2]), reverse=True)
        for rule in sorted_rules:
            pre_course_num = ''
            pre_course_name = ''
            for item in list(list(rule)[0]):
                # ans = db.search_course(item[:-2])
                pre_course_num += item[:-2] + ','
                pre_course_name += db.search_course(item[:-2])[0][1] + ' ~ ' + item[-1:] + ','
            # pre_name = db.search_course(pre_course_num[:-2])
            last_course_num = ''
            last_course_name = ''
            for item in list(list(rule)[1]):
                last_course_num += item[:-2] + ','
                last_course_name += db.search_course(item[:-2])[0][1]+ ' ~ ' + item[-1:] + ','
            # last_name = db.search_course(last_course_num[:-2])
            # print(pre_course_num+"-->"+last_course_num+"    "+str(list(rule)[2]))
            ans.append([support,confidence,pre_course_num,pre_course_name,last_course_num,last_course_name,str(round(list(rule)[2],2)),cur_time])
            i += 1
            # if i >= 3: break
    print(ans)
    db.insert_rules_history(ans)
    # return ans

if __name__ == "__main__":
    main("data/",True)
    # buildRules(0.3,0.6)
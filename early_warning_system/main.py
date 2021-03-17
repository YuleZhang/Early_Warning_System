# -- coding: utf-8
from apriori import Apriori
from Database import DatabaseOperations
import early_warning_system
import pandas as pd
import pymysql
import sys

def load_data(level):
    db = DatabaseOperations()
    res = db.search_student_grade()
    df = pd.DataFrame(list(res),columns=['学号','姓名','年级','班级','课程号','成绩'])
    df = df[((df['年级']=='2015') & (df['成绩']==level))]
    all_student_sum = []
    for name,group in df.groupby('学号'):
        s = [item['课程号']+'-'+item['成绩'] for idx,item in group.iterrows()]
        if len(s) > 1:
            all_student_sum.append(s)
    return all_student_sum

def buildRules():
    level = ['优','良','中','差']
    apr = Apriori()
    db = DatabaseOperations()
    ans = []
    for item in level:
        data = load_data(item)
        L,supportData = apr.apriori(data,minSupport=0.5)
        rules=apr.generateRules(L,supportData,minConf=0.6)
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
            ans.append([pre_course_num,pre_course_name,last_course_num,last_course_name,str(list(rule)[2])])
            i += 1
            if i >= 3: break
    return ans

if __name__ == "__main__":
    # if len(sys.argv) != 2 or sys.argv[1] not in ['console', 'flask']:
        # raise ValueError("""usage: python main.py [console / flask]""")
    print("building rules, please wait!")
    ans = buildRules()
    # if sys.argv[1] == 'console':
    #     for item in ans:
    #         print(item)
    # else:
    #     flaskShow.main(ans)
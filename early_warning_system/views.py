# -*- encoding = utf-8 -*-
from flask import Flask,render_template,redirect,url_for,request,jsonify
from early_warning_system.file_operation import get_FileSize,get_FileCreateTime
from early_warning_system.preprocessing import buildRules,main
from early_warning_system.database import DatabaseOperations
from datetime import timedelta
import time
import os

files_path = 'data/'
db = DatabaseOperations()
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1) # 设置缓存最大时间
num_progress = 0 # 当前的后台进度值

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showRules',methods=['GET','POST'])
def showRules():
    return render_template('main.html')

@app.route('/searchRules',methods=['GET','POST'])
def searchRules():
    if request.method == 'POST':
        result = db.search_rules_history()
        return jsonify(result)
    return render_template('main.html')

@app.route('/generateRules',methods=['GET','POST'])
def getRules():
    global num_progress
    # load the csv data to database
    # if request.method == 'POST':
    # support = request.form.get('support')
    support = request.args.get('support', '')
    confidence = request.args.get('confidence', '')
    print('support',support)
    print('confidence',confidence)
    for i in range(123):
    # ... 数据处理业务
        num_progress = i * 100 / 123; # 更新后台进度值，因为想返回百分数所以乘100
        time.sleep(0.001)
    return redirect('searchRules')
    # basepath = os.path.dirname(__file__)
    # parentpath = os.path.dirname(basepath) #获得d所在的目录,即d的父级目录
    # datapath = os.path.join(os.path.abspath(parentpath),"data")
    # main(datapath,True) # 将表格读取到数据库中
    # buildRules(support,confidence) # 读取数据库根据置信度生成规则存入mysql中
    # return render_template('main.html')
    # return render_template('main.html')

@app.route('/buildRuleProgress',methods=['GET','POST'])
def buildRuleProgress():
    return jsonify(num_progress)

@app.route('/filePages',methods=['GET','POST'])
def filePages():
    return render_template('fileList.html')

@app.route('/searchFiles',methods=['GET','POST'])
def searchFiles():
    result = db.search_file_history()
    print(result)
    return jsonify(result)

@app.route('/uploadFile',methods=['GET','POST'])
def uploadFile():
    if request.method == 'POST':
        f = request.files.get("file")
        if f is None: return render_template('fileList.html')
        basepath = os.path.dirname(__file__)
        parentpath = os.path.dirname(basepath) #获得d所在的目录,即d的父级目录
        upload_path = os.path.join(os.path.abspath(parentpath),"data",f.filename)
        f.save(upload_path)
        print('保存成功',upload_path)
        return redirect(url_for('upload'))
    return render_template('fileList.html')

@app.route('/removeFile',methods=['GET','POST'])
def removeFile():
    if request.method == 'POST':
        fileID = request.form['fileID']
        print(fileID)
        db.delete_file_history(fileID)
        result = db.search_file_history()
        return jsonify(result)
    return render_template('fileList.html')

@app.route('/regist',methods=['GET','POST'])
def regist():
    return render_template('register.html')

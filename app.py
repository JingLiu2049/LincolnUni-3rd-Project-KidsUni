# Imports
################################################
from flask import Flask,url_for,session, redirect, flash,render_template,request, send_from_directory,send_file
import datetime as dt
import time
import psycopg2
from psycopg2.extras import RealDictCursor
import connect
import uuid
import re
from datetime import datetime, timedelta, date 
from dateutil.relativedelta import *
from flask_mail import Mail, Message
import smtplib
import xlrd, xlwt, xlutils
import os
from werkzeug.utils import secure_filename
import openpyxl as op
import pandas as pd
import numpy
import member_info
import db
import zipfile


# Global Functions
################################################
app = Flask(__name__)
app.secret_key = 'project2_kids_uni'
dbconn = None
def getCursor():    
    global dbconn    
    if dbconn == None:
        conn = psycopg2.connect(connect.conn_string)
        dbconn = conn.cursor()  
        #conn.autocommit = True
        return dbconn
    else:
        return dbconn
def conn():
    conn = psycopg2.connect(connect.conn_string)
    return conn

def upload_path(name):
    file = request.files[name]
    filename = secure_filename(file.filename)
    basepath  = os.path.dirname(__file__)
    excelpath = os.path.join(basepath,'uploads',filename)
    file.save(excelpath)
    return excelpath

def test(obj):
    print(obj,type(obj),'tttttttttttttttttttttttttt',datetime.now)


@app.route("/",methods = ['POST','GET'])
def login():
    return render_template('login.html')
@app.route("/index", methods = ['POST','GET'])
def index():
    return render_template("index.html")

@app.route("/member", methods = ['POST','GET'])
def member(): 
    cur = getCursor() 
    cur.execute(f"select * from members ORDER BY school_id, member_id;")
    result=cur.fetchall() 
    column_name = [desc[0] for desc in cur.description]
    if request.method == 'POST':
        return render_template("member.html")
    else:
        return render_template("member.html",result=result, column=column_name)

@app.route("/member_upload", methods = ['POST'])
def member_upload():
    form = request.form
    if form:
        events = request.form.getlist('mem_col')[26:-1]
        i = 0
        while i<len(form)-3:
            mem = request.form.getlist(f'mem{i}')
            member = member_info.mem_obj(mem)
            member.insert_db()
            if events:
                test(member.event)
            i += 1
        coor = request.form.getlist('coor')
        member_info.insert_coor(coor)
        
        return redirect(url_for('member'))
    else:
        excelpath = upload_path('file')
        df_list= member_info.get_df(excelpath)
        df_member = df_list[0]
        df_coor = df_list[1]
        mem_col = df_member.columns
        mem_data = df_member.values
        coor_col = df_coor.columns
        coor_data = df_coor.values
        test(df_coor)
        print(df_member)

        return render_template('member_upload.html',mem_col = mem_col, mem_data = mem_data, 
            coor_col = coor_col, coor_data = coor_data)
@app.route("/generating",methods = ['POST','GET'])   
def generating():
    cur = getCursor()
    cur.execute("SELECT school_id, school_name FROM schools;")
    schools = cur.fetchall()
    
    if request.method == 'POST':
        school_list = request.form.getlist('schools')
        zfile = zipfile.ZipFile(f'{app.root_path}\downloads\Templates.zip','w')
        for schoolid in school_list:
            filename = member_info.gen_endyear_temp(schoolid)
            zfile.write(filename)
        zfile.close()


        return send_file(f'{app.root_path}\downloads\Templates.zip',
            mimetype = 'zip',
            attachment_filename= 'Templates.zip',
            as_attachment = True)


    return render_template('generating.html',schools = schools)
@app.route("/school",methods = ['POST','GET'])
def school():
    return render_template('school.html')     

@app.route("/destination",methods = ['POST','GET'])     
def destination():
    return render_template('destination.html') 

@app.route("/volunteer",methods = ['POST','GET'])     
def volunteer():
    return render_template('volunteer.html')   

@app.route("/event",methods = ['POST','GET'])     
def event():
    return render_template('event.html')  

@app.route("/new_user",methods = ['POST','GET'])     
def new_user():
    return render_template('new_user.html')  
    
       
    



if __name__ == '__main__':
    app.run(debug=True)


# Imports
################################################
from flask import Flask,url_for,session, redirect, flash,render_template,request, send_from_directory
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
from openpyxl import load_workbook
import pandas as pd
import numpy
import member_info


# Global Functions
################################################
app = Flask(__name__)
app.secret_key = 'project2_kids_uni'
dbconn = None
def getCursor():    
    global dbconn    
    if dbconn == None:
        conn = psycopg2.connect(dbname=connect.dbname, user=connect.dbuser, 
        password=connect.dbpass, host=connect.dbhost, port=connect.dbport)
        dbconn = conn.cursor()  
        #conn.autocommit = True
        return dbconn
    else:
        return dbconn

def get_path(name):
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
    cur.execute(f"select * from members;")
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
            member.insert_mem()
            if events:
                test(member.event)
            i += 1
        coor = request.form.getlist('coor')
        member_info.insert_coor(coor)
        
        return redirect(url_for('member'))
    else:
        excelpath = get_path('file')
        wb_list= member_info.get_wb(excelpath)
        wb_member = wb_list[0]
        wb_coor = wb_list[1]
        mem_col = wb_member.columns
        mem_data = wb_member.values
        coor_col = wb_coor.columns
        coor_data = wb_coor.values
        test(wb_coor)
        test(coor_data)

        return render_template('member_upload.html',mem_col = mem_col, mem_data = mem_data, 
            coor_col = coor_col, coor_data = coor_data)
            
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


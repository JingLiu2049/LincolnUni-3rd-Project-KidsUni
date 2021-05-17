# Imports
################################################
from flask import Flask,url_for,session, redirect, flash,render_template,request, send_from_directory,send_file
import datetime as dt
import psycopg2
from psycopg2.extras import RealDictCursor
import connect
import re
from datetime import datetime, timedelta, date 
from dateutil.relativedelta import *
from flask_mail import Mail, Message
import smtplib
import os
from werkzeug.utils import secure_filename
import openpyxl as op
import pandas as pd
import numpy
import member_info
import db
import zipfile
import getid
import spreadsheet
import uuid


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
        
# uploaded file, rename and get path
def upload_path(name):
    file = request.files[name]
    filename = secure_filename(file.filename)
    basepath  = os.path.dirname(__file__)
    excelpath = os.path.join(basepath,'uploads',filename)
    file.save(excelpath)
    return excelpath

def test(obj):
    print(obj,type(obj),'tttttttttttttttttttttttttt',datetime.now)

# Generate ID
def genID():
    return uuid.uuid4().fields[1]

# App Route
##################################################
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
    # get data from client-side and insert into database
    if form:
        event_ids = request.form.getlist('mem_col')[25:-1]
        i = 0
        while i<len(form)-3:
            mem = request.form.getlist(f'mem{i}')
            member = member_info.mem_obj(mem)
            member.insert_db(event_ids)
            i += 1
        coor = request.form.getlist('coor')
        member_info.insert_coor(coor)
        
        return redirect(url_for('member'))
    #  read uploaded excel file and send info to client-side
    else:
        excelpath = upload_path('file')
        df_list= member_info.get_df(excelpath)
        df_member = df_list[0]
        df_coor = df_list[1]
        mem_col = df_member.columns
        mem_data = df_member.values
        coor_col = df_coor.columns
        coor_data = df_coor.values

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
    cur = db.getCursor()
    cur.execute("SELECT * FROM events ORDER BY event_id")
    events = cur.fetchall()
    return render_template('event.html',events = events) 
@app.route("/add_event",methods =['POST','GET']) 
def add_event():
    # get added event info from client-side and insert into database
    if request.method == 'POST':
        names = request.form.getlist('name')
        event_dates = request.form.getlist('event_date')
        locations = request.form.getlist('location')
        notes = request.form.getlist('note')
        for i in range(0,len(names)):
            cur = db.getCursor()
            sql = "INSERT INTO events VALUES(nextval('eventid_seq'),'%s','%s','%s',\
                '%s');" %(names[i],event_dates[i],locations[i],notes[i])
            cur.execute(sql)
        return redirect(url_for('event'))


    return render_template('add_event.html')

@app.route("/new_user",methods = ['POST','GET'])     
def new_user():
    if request.method == 'POST':
        user_id = genID()
        firstname = request.form.get('firstname')
        surname = request.form.get('surname')
        email = request.form.get('email')
        phonenumber = request.form.get('phonenumber')
        print(user_id)
        print(firstname)
        print(surname)
        print(email)
        print(phonenumber)
        
        cur = getCursor()              
        cur.execute("INSERT INTO admin(user_id, first_name, surname, phone_number, email) VALUES (%s,%s,%s,%s,%s);",(int(user_id), firstname, surname, phonenumber, email,))
        cur.execute("INSERT INTO authorisation(user_id, username) VALUES (%s,%s);",(user_id, email,))
        return redirect("/")
    else:
        return render_template('new_user.html')  

@app.route("/download", methods = ['POST','GET'])
def download():
    return render_template('download.html')
# generating excel file of member for downloading
@app.route("/download_mem_sheet",methods = ['POST','GET'])   
def download_mem_sheet():
    # spreadsheets are differed based on different schools, get school info and display on clined-side for selecting
    cur = getCursor()
    cur.execute("SELECT school_id, school_name FROM schools;")
    schools = cur.fetchall()
    # get selected info from clined-side
    if request.method == 'POST':
        request_file = request.form.get('type')
        school_list = request.form.getlist('schools')
    # generating excel of black template and send to client-side
        if request_file =='template':
            zfile = zipfile.ZipFile(f'{app.root_path}\downloads\Templates.zip','w')
            for schoolid in school_list:
                filename = spreadsheet.gen_mem_temp(schoolid,f'{request_file}')
                zfile.write(filename)
            zfile.close()
            return send_file(f'{app.root_path}\downloads\Templates.zip',
                mimetype = 'zip',
                attachment_filename= 'Templates.zip',
                as_attachment = True)
    # generating excel with completed data and send to client-side
        elif request_file =='completed':
            zfile = zipfile.ZipFile(f'{app.root_path}\downloads\Competed.zip','w')
            for schoolid in school_list:
                filename = spreadsheet.gen_mem_temp(schoolid,f'{request_file}')
                zfile.write(filename)
            zfile.close()
            return send_file(f'{app.root_path}\downloads\Competed.zip',
                mimetype = 'zip',
                attachment_filename= 'Competed.zip',
                as_attachment = True)

    return render_template('download_mem_sheet.html',schools = schools)



    



if __name__ == '__main__':
    app.run(debug=True)


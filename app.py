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



@app.route("/", methods = ['POST','GET'])
def index():
    return render_template("index.html")
@app.route("/member", methods = ['POST','GET'])
def member():
    
    return render_template("member.html")


@app.route("/member_upload", methods = ['POST','GET'])
def member_upload():
    if request.method =='POST':
        
        form = request.form
        if form:
            
            for i in  form:
                mem = request.form.getlist(f'{i}')
                print(mem)
                
            return redirect(url_for('member'))
        else:
            excelpath = get_path('file')
            wb_school = pd.read_excel(excelpath,0,header=None,nrows=3)
            wb_school.dropna(axis='columns',how='all',inplace=True)
            name = wb_school.loc[0,3]
            print(name)
            wb1 = pd.read_excel(excelpath,0,header=[5])
            wb1['2020 Hours     (if applicable)'].fillna('na', inplace=True)
            wb1.rename(columns={'#':'Memberid'},inplace = True)
            
            
            wb2 = pd.read_excel(excelpath,1,header=[5])
            wb_joined = pd.concat([wb1,wb2[['USERNAME','PASSWORD']]],axis=1)
            wb_joined.loc[:,'School name'] = name
            wb_joined.loc[:,'index'] = wb_joined.index
            columns = wb_joined.columns


            # print(wb1[['First Name','Last Name']],'dddddddddddddddd')

            # wb1.loc[wb1['memberid']/100000 < 1, 'memberid'] = member_info.get_id()


            # ids = []
            # for item in data:
            #     if item[0]/100000 < 1:
            #         id = member_info.get_id()
            #         ids.append(id)
            # wb1.loc[:,'memberid'] = ids
            # print(ids,'iiiiiiiiiiiiiiiiiiiiiiiii')
            data = wb_joined.values

            print(wb_joined,'111111111111111111111111')
            # print(wb4,'111111111111111111111111')

            

            return render_template('member_upload.html',data = data,columns = columns)
            
            
    
       
    



if __name__ == '__main__':
    app.run(debug=True)


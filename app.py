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


@app.route("/", methods = ['POST','GET'])
def index():
    return render_template("index.html")
@app.route("/member", methods = ['POST','GET'])
def member():
    
    return render_template("member.html")

    
@app.route("/member_upload", methods = ['POST','GET'])
def member_upload():
    if request.method =='POST':
        file = request.files['file']
        form = request.form
        print(form,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')
        print(file,'llllllllllllllllllllllllllllllllllllllllllllllllllllllll')
        if form:
            return redirect(url_for('member'))
            
        else:
            filename = secure_filename(file.filename)
            basepath  = os.path.dirname(__file__)
            excelpath = os.path.join(basepath,'uploads',filename)
            file.save(excelpath)
            wb = pd.read_excel(excelpath)
            data = wb.iloc[4:].values
            return render_template('member_upload.html',data = data)
            
            
    
       
    



if __name__ == '__main__':
    app.run(debug=True)


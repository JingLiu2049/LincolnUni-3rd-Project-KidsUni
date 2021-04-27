from flask import Flask,url_for,session, redirect, flash,render_template,request
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


@app.route("/")
def index():
    pass


if __name__ == '__main__':
    app.run(debug=True)


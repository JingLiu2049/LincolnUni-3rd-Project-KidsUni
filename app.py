# Imports
################################################
from flask import Flask, url_for, session, redirect, flash, render_template, request, send_file,make_response
import psycopg2
from psycopg2.extras import RealDictCursor, NamedTupleCursor
import connect
import re
from datetime import datetime, time, timedelta, date
from dateutil.relativedelta import *
from flask_mail import Mail, Message
import smtplib
import os
from werkzeug.utils import secure_filename
import pandas as pd
import db
import zipfile
import spreadsheet
import uuid
import uploads
import schools_info, member_info, destinations
from functools import wraps
import classes



# Global Functions
################################################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'project2_kids_uni'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=30)



#app.secret_key = 'project2_kids_uni'
dbconn = None


def getCursor():
    global dbconn
    if dbconn == None:
        conn = psycopg2.connect(connect.conn_string)
        conn.autocommit = True
        dbconn = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        return dbconn
    else:
        return dbconn

# uploaded file, rename and get path


def upload_path(name):
    file = request.files[name]
    filename = secure_filename(file.filename)
    basepath = os.path.dirname(__file__)
    excelpath = os.path.join(basepath, 'uploads', filename)
    file.save(excelpath)
    return excelpath

def test(obj):
    print(obj, type(obj), 'tttttttttttttttttttttttttt', datetime.now)

# Generate ID
def genID():
    return uuid.uuid4().fields[1]


def login_required(f):
    @wraps(f)
    def secure_function(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            flash(f'Please login to access this page.', 'danger')
            return redirect(url_for('login', next=request.url))
    return secure_function
# Disable browser downloads from cache
def no_cache(fun):
    @wraps(fun)
    def inner(*args,**kwargs):
        response = make_response(fun(*args,**kwargs))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" 
        response.headers["Pragma"] = "no-cache" 
        response.headers["Expires"] = "0"
        return response
    return inner

# App Route
##################################################

# This will be the login page, we need to use both GET and POST requests


@app.route('/', methods=['GET', 'POST'])
def login():

    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        next_url = request.form.get('next')
        remember_me = request.form.get('remember_me')
        print(username)
        print(next_url)
        print(remember_me)
        # Check if account exists using MySQL
        cur = db.getCursor()
        cur.execute('SELECT * FROM authorisation WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cur.fetchone()
        # print(account)
        # print(account[0])
        # print(type(account[0]))

        cur.execute('SELECT status FROM admin WHERE user_id = %s',(int(account[0]),))
        status = cur.fetchone()
        print(status)
        # If account exists in accounts table in our database
        if account and status[0] == 'active':
            sql = "SELECT first_name, surname FROM admin JOIN authorisation ON admin.user_id=authorisation.user_id \
                WHERE authorisation.user_id = %s;" % account[0]
            cur.execute(sql)
            name = cur.fetchone()
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['user_id'] = account[0]
            session['username'] = account[1]
            session['name'] = name
            session['remember_me'] = True if request.form.get(
                'remember_me') else False
            print(session['remember_me'])
            if next_url:
                return redirect(next_url)
            # Redirect to home page
            return redirect(url_for('index'))
        if account and status[0] == 'deactivated':
            flash(
                f'Login unsuccessful. Please contact admin to check your account.', 'danger')
            return redirect(url_for('login'))
        else:
            # Account doesnt exist or username/password incorrect
            flash(f'Login Unsuccessful. Please check your email and password!', 'danger')
    return render_template('login.html', title='Login')


# This will be the logout page
@app.route('/logout')
@login_required
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('remember', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route("/index", methods=['POST', 'GET'])
@login_required
def index():
    total_members = member_info.active_members_count()
    total_members_hours = member_info.total_members_hours()
    active_schools = schools_info.active_schools_count()
    in_progress_schools = schools_info.in_progress_schools_count()
    total_schools = schools_info.total_schools_count()
    active_destinations = destinations.active_destinations_count()
    pending_destinations = destinations.pending_destinations_count()
    total_destinations = destinations.total_destinations_count()
    return render_template("index.html", name=session['name'], total_members=total_members,
        total_members_hours=total_members_hours, active_schools=active_schools, in_progress_schools=in_progress_schools,
        total_schools=total_schools, active_destinations=active_destinations, pending_destinations=pending_destinations,
        total_destinations=total_destinations)


@app.route("/member", methods=['POST', 'GET'])
@login_required
def member():
    cur = db.getCursor()
    cur.execute("select * from member_info;")
    result = cur.fetchall()
    date=datetime.today().year
    if request.method == 'POST':

        return render_template("member.html", name=session['name'])
    else:
        return render_template("member.html",result=result, date=date, name=session['name'])

@app.route("/member_filter", methods=['POST'])
@login_required
def member_filter():
    if request.method == 'POST':
        cur = db.getCursor()
        school = request.form.get('schoolfilter')

        cur.execute(f"select * from member_info where school_name='{school}';")
        filter_result = cur.fetchall()
        return render_template("member.html", name=session['name'], filter=filter_result)
    else:
        return redirect(url_for(member))


@app.route("/member_upload", methods=['POST'])
@login_required
def member_upload():
    form = request.form
    # get data from client-side and insert into database
    if form:
        coor = request.form.getlist('coor')
        uploads.insert_coor(coor)
        events = request.form.getlist('mem_col')[25:-1]
        for i in range(0, len(form)-3):
            mem = request.form.getlist(f'mem{i}')
            mem.insert(25,coor[-1]) # insert collecting date for the data
            member = uploads.mem_obj(mem)
            member.insert_db(events)
        return redirect(url_for('member'))
    #  read uploaded excel file and send info to client-side
    else:
        excelpath = upload_path('file')
        try:
            df_list= uploads.get_mem_df(excelpath)
            df_member = df_list[0]
            df_coor = df_list[1]
            mem_col = df_member.columns
            mem_data = df_member.values
            coor_col = df_coor.columns
            coor_data = df_coor.values
        except Exception as e:
            # return render_template('error.html', name=session['name'])
            return print(e)
        return render_template('member_upload.html', mem_col=mem_col, mem_data=mem_data,
                    coor_col=coor_col, coor_data=coor_data, name=session['name'])

        


@app.route("/school", methods=['POST', 'GET'])
@login_required
def school():
    cur = db.getCursor()
    cur.execute("select * from schools;")
    result = cur.fetchall()
    cur.execute("select distinct school_name from schools;")
    school_name = cur.fetchall()
    school_filter = school_name
    cur.execute("select distinct who from schools;")
    who = cur.fetchall()
    cur.execute("select distinct council from schools;")
    council = cur.fetchall()
    cur.execute("select distinct category from schools;")
    category = cur.fetchall()
    cur.execute("select distinct status from schools;")
    status = cur.fetchall()
    cur.execute("select distinct returning_number from schools order by returning_number asc;;")
    returning_number = cur.fetchall()
    cur.execute("select distinct max_num_2021 from schools order by max_num_2021 asc;;")
    max_num_2021= cur.fetchall()
    cur.execute("select distinct confirmed_num from schools order by confirmed_num asc;;")
    confirmed_num = cur.fetchall()
    cur.execute("select distinct training from schools;")
    training = cur.fetchall()
    cur.execute("select distinct launch from schools;")
    launch = cur.fetchall()
    cur.execute("select distinct passport_presentation from schools;")
    passport_presentation = cur.fetchall()
    cur.execute("select distinct portal from schools;")
    portal = cur.fetchall()
    cur.execute("select distinct passports from schools;")
    passports = cur.fetchall()
    cur.execute("select distinct agreement from schools;")
    agreement = cur.fetchall()
    cur.execute("select distinct consent from schools;")
    consent = cur.fetchall()
    cur.execute("select distinct notes from schools;")
    notes = cur.fetchall()
    date = datetime.today().year

    if request.method == 'POST':

        return render_template("school.html", name=session['name'])
    else:
        return render_template("school.html", result=result, date=date, school_filter=school_filter,
                               school_name=school_name, who=who, council=council, category=category, status=status, 
                               returning_number=returning_number, max_num_2021=max_num_2021, confirmed_num=confirmed_num,
                               training=training, launch=launch, passport_presentation=passport_presentation, portal=portal,
                                passports=passports, agreement=agreement, consent=consent,notes=notes, name=session['name'])

@app.route("/school_filter", methods=['POST'])
@login_required
def school_filter():
    if request.method == 'POST':
        cur = db.getCursor()
        school = request.form.get('schoolfilter')

        cur.execute(f"select * from schools where school_name='{school}';")
        filter_result = cur.fetchall()
        return render_template("school.html", name=session['name'], filter=filter_result)
    else:
        return redirect(url_for('school'))

@app.route("/school_upload", methods=['POST'])
@login_required
def school_upload():
    form = request.form
    # get data from client-side and insert into database
    if form:
        total = request.form.getlist('school_col')[18:-1]
        for i in range(0, len(form)-1):
            school_info = request.form.getlist(f'school{i}')
            school_obj = schools_info.school_obj(school_info[:-1])
            school_obj.insert_db()
        return redirect(url_for('school'))
    #  read uploaded excel file and send info to client-side
    else:
        excelpath = upload_path('file')
        try:
            df_school = schools_info.get_df(excelpath)
            school_cols = df_school.columns
            school_data = df_school.values

        except Exception as e:
            # return render_template('error.html')
            return print(e)
        return render_template('school_upload.html', cols=school_cols, data=school_data, name=session['name'])


@app.route("/destination", methods=['POST', 'GET'])
@login_required
def destination():
    cur = db.getCursor()
    cur.execute("SELECT * FROM destinations ORDER BY ld_id;")
    dests = cur.fetchall()
    return render_template('destination.html', dests=dests, name=session['name'])


@app.route("/destination_upload", methods=['POST'])
@login_required
def destination_upload():
    form = request.form
    # get data from client-side and insert into database
    if form:
        paperwork = request.form.getlist('des_col')[20:-1]
        print(paperwork,'ppppppppppppppppppppppppp')
        for i in range(0,len(form)-1):
            dest_info = request.form.getlist(f'des{i}')
            print(dest_info[:-1])
            dest_obj = uploads.dest_obj(dest_info[:-1])
            print(dest_obj.paperwork)
            dest_obj.insert_db(paperwork)
        return redirect(url_for('destination'))
    #  read uploaded excel file and send info to client-side
    else:
        excelpath = upload_path('file')
        try:
            df_dest = uploads.get_dest_df(excelpath)
            # df_dest = pd.read_excel(excelpath,0,header=[1])
            dest_cols = df_dest.columns
            dest_data = df_dest.values
            print(df_dest.iloc[:,15:19])
            
        except Exception as e:
            # return render_template('error.html')
            return print(e)
        return render_template('destination_upload.html',cols = dest_cols, data = dest_data, name=session['name'])

@app.route("/volunteer", methods=['POST', 'GET'])
@login_required
def volunteer():
    cur = db.getCursor()
    def get_criteria(d={}):
        criteria = {}
        for i in d.keys():
            cur.execute(f"SELECT DISTINCT {d[i][0]} FROM {d[i][1]} WHERE {d[i][0]} IS NOT null;")
            results = cur.fetchall()
            value_list = []
            if len(results) > 1:
                for j in results:
                    value_list.append(j) if j != None else False
            else:
                value_list =[results[0][0]] if results != None else []
            criteria.setdefault(i,value_list)
        return criteria

    volun_criteria_dict= {
        'Status':['status','volun_detail'],
        'Induction':['induction','volun_detail'],
        'Interview':['interview','volun_detail'],
        'Gender':['gender','volun_detail'],
        'Volunteer Experience':['experience','volun_detail'],
        'Future Leader':['future_leader','volun_detail'],
        'Police Check':['police_check','volun_detail'],
        'University':['studying_uni','volun_detail'],
        'Course':['course','volun_detail'],
        'Current Year':['current_year','volun_detail'],
        'Completion Date':['completion_date','volun_detail']
        }
    filter_criteria = get_criteria( volun_criteria_dict )
    if request.method == 'POST':
        form = request.form.to_dict()
        query = ''
        count = 0
        for i in form.keys():
            column = volun_criteria_dict[i][0]
            values = request.form.getlist(i)
            for j in range(0,len(values)):
                if count == 0 and j == 0:
                    query += f"{column} = '{values[j]}'"
                elif j == 0:
                    query += f" AND {column} = '{values[j]}'"
                else:
                    query += f" OR {column} = '{values[j]}'"
            count += 1

        sql = f'SELECT * FROM volun_detail WHERE {query} ORDER BY volun_id;'
    else:
        sql ="SELECT * FROM volun_detail ORDER BY volun_id;"

    def get_volun_list(results):
        volun_list = []
        for i in results:
            volun = list(i)
            volun_obj = classes.volunteer(volun)
            volun_list.append(volun_obj)
        return volun_list
    cur.execute(sql)
    results = cur.fetchall()
    volun_list = get_volun_list(results)
    return render_template('volunteer.html', name=session['name'], voluns=volun_list, criteria = filter_criteria)


@app.route("/volunteer_upload", methods=['POST', 'GET'])
@login_required
def volunteer_upload():
    form = request.form
    # get data from client-side and insert into database
    if form:
        events = request.form.getlist('col')[38:-1]
        for i in range(0,len(form)-1):
            volun_info = request.form.getlist(f'index{i}')
            volun_obj = uploads.volun_obj(volun_info)
            volun_obj.insert_db(events)
        return redirect(url_for('volunteer'))
    else:
        excelpath = upload_path('file')
        try:
            df_volun = uploads.get_volun_df(excelpath)
            volun_cols = df_volun.columns
            volun_data = df_volun.values

            
        except Exception as e:
            # return render_template('error.html')
            return print(e)
        return render_template('volunteer_upload.html', cols=volun_cols, data=volun_data, name=session['name'])


@app.route("/event", methods=['POST', 'GET'])
@login_required
def event():
    cur = db.getCursor()
    cur.execute("SELECT events.*, event_attend.number,volun_attend.attend FROM events\
        LEFT JOIN event_attend ON events.event_id = event_attend.event_id LEFT JOIN \
        volun_attend ON events.event_id = volun_attend.event_id ORDER BY events.event_date DESC;")
    events = cur.fetchall()
    print(events,'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    return render_template('event.html', events=events, name=session['name'])


@app.route("/edit_event", methods=['POST', 'GET'])
@login_required
def edit_event():
    cur = db.getCursor()
    if request.method == 'POST':
        event = request.form.to_dict()
        sql = "UPDATE events SET name = '%s', event_date = '%s', location = '%s', description = '%s' \
            WHERE event_id = %s" % (event['name'], event['event_date'], event['location'], event['description'], int(event['id']))
        cur.execute(sql)
        return redirect(url_for('event'))
    else:
        eventid = int(request.args.get('eventid'))
        operation = request.args.get('oper')
        if operation == 'edit':
            cur.execute(
                "SELECT * FROM events WHERE event_id = %s;", (eventid,))
            eventinfo = cur.fetchone()
            return render_template("edit_event.html", eventinfo=eventinfo, name=session['name'])
        elif operation == 'delete':
            try:
                cur.execute(
                    "DELETE FROM events WHERE event_id = %s;", (eventid,))
            except:
                cur.execute(
                    "DELETE FROM attendance WHERE event_id = %s;", (eventid,))
                cur.execute(
                    "DELETE FROM volun_hours WHERE event_id = %s;", (eventid,))
                cur.execute(
                    "DELETE FROM events WHERE event_id = %s;", (eventid,))
            return redirect(url_for('event'))


@app.route("/add_event", methods=['POST', 'GET'])
@login_required
def add_event():
    # get added event info from client-side and insert into database
    if request.method == 'POST':
        names = request.form.getlist('name')
        event_dates = request.form.getlist('event_date')
        locations = request.form.getlist('location')
        descriptions = request.form.getlist('description')
        for i in range(0, len(names)):
            cur = db.getCursor()
            sql = "INSERT INTO events VALUES(nextval('eventid_seq'),'%s','%s','%s',\
                '%s');" % (names[i], event_dates[i], locations[i], descriptions[i])
            cur.execute(sql)
        return redirect(url_for('event'))
    return render_template('add_event.html', name=session['name'])


@app.route("/users", methods=['POST', 'GET'])
@login_required
def users():
    cur = db.getCursor()
    cur.execute("SELECT * FROM admin ORDER BY surname;")
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    return render_template('users.html', users=select_result, dbcols=column_names, name=session['name'])


@app.route("/edit_user", methods=['POST', 'GET'])
@login_required
def edit_user():
    cur = db.getCursor()
    if request.method == 'POST':
        current_status = request.form.get('current_status')
        updated_status = request.form.get('updated_status')

        print(current_status)
        print(updated_status)
        if updated_status == None:
            user = request.form.to_dict()
            sql = "UPDATE admin SET first_name = '%s', surname = '%s', phone_number = '%s', email = '%s' \
                WHERE user_id = %s" % (user['first_name'], user['surname'], user['phone_number'], user['email'],
                                       int(user['user_id']))
            cur.execute(sql)
            flash(f'User successfully updated.', 'success')
            return redirect(url_for('users'))
        if updated_status == 'deactivated' or updated_status == 'active':
            user = request.form.to_dict()
            sql = "UPDATE admin SET first_name = '%s', surname = '%s', phone_number = '%s', email = '%s', status = '%s' \
                WHERE user_id = %s" % (user['first_name'], user['surname'], user['phone_number'], user['email'], user['updated_status'], int(user['user_id']))
            cur.execute(sql)
            flash(f'User successfully updated.', 'success')
            return redirect(url_for('users'))
    else:
        user_id = request.args.get('user_id')
        cur.execute("SELECT * FROM admin WHERE user_id = %s;", (user_id,))
        userinfo = cur.fetchone()
        return render_template("edit_user.html", userinfo=userinfo, name=session['name'])


@app.route("/add_user", methods=['POST', 'GET'])
@login_required
def add_user():
    if request.method == 'POST':
        user_id = genID()
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        status = "active"
        print(user_id)
        print(first_name)
        print(surname)
        print(email)
        print(phone_number)

        cur = db.getCursor()
        cur.execute("INSERT INTO admin(user_id, first_name, surname, phone_number, email, status) VALUES (%s,%s,%s,%s,%s,%s);",
                    (int(user_id), first_name, surname, phone_number, email, status,))
        cur.execute(
            "INSERT INTO authorisation(user_id, username) VALUES (%s,%s);", (user_id, email,))
        flash(f'User successfully added!', 'success')
        return redirect(url_for('users'))
    return render_template('add_user.html', name=session['name'])


@app.route("/download", methods=['POST', 'GET'])
@login_required
def download():
    return render_template('download.html', name=session['name'])

# generating excel file of member for downloading
@app.route("/download_mem_sheet", methods=['POST', 'GET'])
@login_required
@no_cache
def download_mem_sheet():
    # spreadsheets are differed based on different schools, get school info and display on clined-side for selecting
    cur = db.getCursor()
    cur.execute("SELECT school_id, school_name FROM schools;")
    schools = cur.fetchall()
    # get selected info from clined-side
    if request.method == 'POST':
        request_file = request.form.get('type')
        school_list = request.form.getlist('schools')
    # generating excel of black template and send to client-side
        if request_file == 'template':
            zfile = zipfile.ZipFile(
                f'{app.root_path}\downloads\Templates.zip', 'w')
            for schoolid in school_list:
                filename = spreadsheet.gen_mem_tmp(schoolid)
                zfile.write(filename)
            zfile.close()
            return send_file(f'{app.root_path}\downloads\Templates.zip',
                             mimetype='zip',
                             attachment_filename='Templates.zip',
                             as_attachment=True)
    # generating excel with completed data and send to client-side
        elif request_file == 'completed':
            zfile = zipfile.ZipFile(
                f'{app.root_path}\downloads\Competed.zip', 'w')
            for schoolid in school_list:

                filename = spreadsheet.gen_mem_comp(schoolid)
                zfile.write(filename)
            zfile.close()
            return send_file(f'{app.root_path}\downloads\Competed.zip',
                             mimetype='zip',
                             attachment_filename='Competed.zip',
                             as_attachment=True)
    return render_template('download_mem_sheet.html', schools=schools, name=session['name'])



@app.route("/download_dest_sheet", methods=['POST', 'GET'])
@login_required
@no_cache
def download_dest_sheet():
    file = spreadsheet.gen_dest_sheet()
    return send_file(file, mimetype = 'xlsx', as_attachment=True)

@app.route("/download_volun_sheet", methods=['POST', 'GET'])
@login_required
@no_cache
def download_volun_sheet():
    file = spreadsheet.gen_volun_sheet()
    return send_file(file, mimetype = 'xlsx', as_attachment=True)


# @app.route("/school_upload",methods = ['POST'])
# @login_required
# def school_upload():
#     form = request.form
#     # get data from client-side and insert into database
#     if form:
#         # coor = request.form.getlist('coor')
#         # member_info.insert_coor(coor)
#         # events = request.form.getlist('mem_col')[25:-1]
#         # for i in range(0,len(form)-3):
#         #     mem = request.form.getlist(f'mem{i}')
#         #     mem.insert(25,coor[-1]) # insert collecting date for the data
#         #     member = member_info.mem_obj(mem)
#         #     member.insert_db(events)
#         # return redirect(url_for('member'))
#         pass
#     #  read uploaded excel file and send info to client-side
#     else:
#         excelpath = upload_path('file')
#         try:
#             df_des = pd.read_excel(excelpath,0)
#             df_des.fillna('',inplace=True)
#             dest_cols = df_des.columns
#             dest_data = df_des.values

#             print(df_des)
#             # df_list= member_info.get_df(excelpath)
#             # df_member = df_list[0]
#             # df_coor = df_list[1]
#             # mem_col = df_member.columns
#             # mem_data = df_member.values
#             # coor_col = df_coor.columns
#             # coor_data = df_coor.values
#         except Exception as e:
#             # return render_template('error.html')
#             return print(e)

#         # return render_template('member_upload.html',mem_col = mem_col, mem_data = mem_data, 
#         #     coor_col = coor_col, coor_data = coor_data)
#         return render_template('school_upload.html',cols = dest_cols, data = dest_data, name=session['name'])










if __name__ == '__main__':
    app.run(debug=True)

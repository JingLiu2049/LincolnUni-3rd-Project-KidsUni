# Imports
################################################
from flask import Flask, url_for, session, redirect, flash, render_template, request, send_file, make_response
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
import uploads, schools_info, member_info, destinations, login_session, classes, filter_info
from functools import wraps


# Global Functions
################################################
app = Flask(__name__)
app.config['SECRET_KEY'] = 'project2_kids_uni'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=30)


# app.secret_key = 'project2_kids_uni'
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


def admin_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['user_access'] == "admin":
            return f(*args, **kwargs)
        else:
            flash(f"You don't have access to this page.", 'danger')
            return redirect(url_for('index'))
    return decorated_function


# Disable browser downloads from cache
def no_cache(fun):
    @wraps(fun)
    def inner(*args, **kwargs):
        response = make_response(fun(*args, **kwargs))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return inner


# if school_id == school_id, update member info database, otherwise add a new member
def upsertMember(form, member_id, school_id):
    first_name = form.first_name.data
    last_name = form.last_name.data
    username = form.username.data
    gender = form.gender.data
    ethnicity = form.ethnicity.data
    member_age = form.age.data
    password = form.password.data
    continuing_new = form.continuing_new.data
    previous = form.previous_hours.data
    passport_number = form.passport_number.data
    passport_date_issued = form.passport_date.data
    ethnicity_info = form.ethnicity_info.data
    teaching_research = form.teaching_research.data
    publication_promos = form.publication_promos.data
    social_media = form.social_media.data
    gown_size = form.gown_size.data
    hat_size = form.hat_size.data
    total = form.total_hours.data
    status = form.status.data
    cur = db.getCursor()
    if member_id != "new":
        cur.execute("Update members set school_id=%s, first_name=%s, last_name=%s, \
                username=%s, password=%s, gender=%s, member_age=%s, ethnicity=%s, continuing_new=%s, passport_number=%s,\
                previous=%s, passport_date_issued=%s, ethnicity_info=%s, teaching_research=%s, publication_promos=%s, \
                social_media=%s, total=%s, gown_size=%s, hat_size=%s, status=%s where member_id=%s;",
                    (school_id, first_name, last_name, username, password, gender, member_age, ethnicity, continuing_new, passport_number,
                     previous, passport_date_issued, ethnicity_info, teaching_research, publication_promos, social_media, total, gown_size,
                     hat_size, status, member_id))
    else:
        cur.execute("INSERT INTO members VALUES(nextval('membered_seq'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                    %s,%s,%s,%s,%s,%s,%s,%s);", (school_id, first_name, last_name, username, password, gender, member_age, ethnicity, continuing_new, passport_number,
                    previous, passport_date_issued, ethnicity_info, teaching_research, publication_promos, social_media, total, gown_size,
                    hat_size, status))


def upsertDestinations(form, ld_id):
    status = form.status.data
    ld_name = form.ld_name.data
    contact_person = form.contact_person.data
    position = form.ld_position.data
    address = form.address.data
    region = form.region.data
    postal_address = form.postal_address.data
    email = form.email.data
    phone_number = form.phone_number.data
    web_address = form.web_address.data
    member_cost = form.member_cost.data
    adult_cost = form.adult_cost.data
    agrt_signed = form.agrt_signed.data
    rov_signed = form.rov_signed.data
    poster_sent = form.poster_sent.data
    logo_sent = form.logo_sent.data
    promo = form.promo.data
    photo = form.photo.data
    note = form.note.data
    cur = db.getCursor()
    if ld_id != "new":
        cur.execute(" Update destinations set status=%s, ld_name=%s, contact_person=%s, ld_position=%s, \
            address=%s, region=%s,  postal_address=%s, phone_number=%s, email=%s, web_address=%s, member_cost=%s,\
            adult_cost=%s, agrt_signed=%s, rov_signed=%s, poster_sent=%s, logo_sent=%s,  promo=%s, photo=%s , note=%s where ld_id=%s;",
                    (status, ld_name, contact_person, position, address, region, postal_address, phone_number, email, web_address,
                     member_cost, adult_cost, agrt_signed, rov_signed, poster_sent, logo_sent, promo, photo, note, ld_id))
    else:
        cur.execute("INSERT INTO destinations VALUES(nextval('destinationid_seq'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
            %s,%s,%s,%s,%s,%s,%s);", (status, ld_name, contact_person, position, address, region, postal_address, phone_number, email,
                                      web_address, member_cost, adult_cost, agrt_signed, rov_signed, poster_sent, logo_sent, promo, photo, note))

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
        cur.execute(
            'SELECT * FROM authorisation WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cur.fetchone()
        if account == None:
            # If account doesn't exist, user receives this error message.
            flash(f'Login Unsuccessful. Please check your email and password!', 'danger')
            return redirect(url_for('login'))
        else:
            # If account exists
            if account:
                cur.execute('SELECT * FROM admin WHERE user_id = %s',
                            (int(account[0]),))
                user = cur.fetchone()
                print(user)
                # If account exists and account is deactivated, user will receive error message
                if user[5] == 'deactivated':
                    flash(
                        f'Login unsuccessful. Please contact admin to check your account.', 'danger')
                    return redirect(url_for('login'))
                # If account exists and account is active, system can log user in
                if user[5] == 'active':
                    session['loggedin'] = True
                    session['user_id'] = account[0]
                    session['username'] = account[1]
                    session['name'] = user[1]
                    session['user_access'] = account[3]
                    session['remember_me'] = True if request.form.get(
                        'remember_me') else False
                    print(session['remember_me'])
                    print(session['user_access'])
                    # If the user tried to access a certain page but wasn't logged in, the system will redirect the user to
                    # this page once they have logged in
                    if next_url:
                        return redirect(next_url)
                    # Redirect to home page
                    return redirect(url_for('index'))
    return render_template('login.html', title='Login')

# This will be the logout page


@app.route('/logout')
@login_required
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('name', None)
    session.pop('user_access', None)
    session.pop('remember_me', None)

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


@app.route("/member", methods=['GET'])
@login_required
def member():
    cur = getCursor()
    cur.execute("select member_id, school_name, concat(first_name,' ' ,last_name) as name, username, gender, member_age, ethnicity, continuing_new, passport_number,\
                   passport_date_issued, ethnicity_info, teaching_research, publication_promos, social_media, gown_size,\
                   hat_size from member_info where status !='Deactive' ;")  # display the member database table in students' page
    result = cur.fetchall()
    return render_template("member.html", result=result, name=session['name'])


# click member id's <tr> to edit member info
# return to member page, reset form, submit
@app.route("/edit_member", methods=['POST', 'GET'])
@login_required
def edit_member():
    cur = getCursor()
    member_id = request.args.get('id')
    form = member_info.MemberInfoForm()  # import flask form member_info.py
    cur.execute(f"select * from member_info where member_id={member_id};")
    member = cur.fetchone()
    school_name = request.form.get('school_name')
    cur.execute(f"select year, term1, term2, term3, term4, total from mem_hour_detail where member_id={member_id};")
    hour_result=cur.fetchall()
    if request.method == 'POST':
        if form.validate_on_submit():
            # create a currently school list from database with school table
            schoolArray = []
            cur.execute(f"select school_name from schools;")
            for row in cur.fetchall():
                schoolArray.append(str(row.school_name))
            if school_name in schoolArray:  # the new school cannot be update if its not in the school list
                cur.execute(
                    f"select school_id from schools where school_name='{school_name}';")
                result = cur.fetchall()
                school_id = result[0]
                upsertMember(form, member_id, school_id)
                message = 'Update successful'
                return render_template('edit_member.html', name=session['name'], form=form, message=message, member=member,hour_result=hour_result)
            else:
                # if the school is not in the list, print error
                print(form.errors)
                return render_template('edit_member.html', name=session['name'], form=form, member=member,hour_result=hour_result)
        else:
            print(form.errors)
            return render_template('edit_member.html', name=session['name'], form=form, member=member,hour_result=hour_result)
    else:
        form.first_name.data = member.first_name
        form.last_name.data = member.last_name
        form.school_name.data = member.school_name
        form.username.data = member.username
        form.gender.data = member.gender
        form.ethnicity.data = member.ethnicity
        form.age.data = member.member_age
        form.password.data = member.password
        form.continuing_new.data = member.continuing_new
        form.previous_hours.data = member.previous
        form.passport_number.data = member.passport_number
        form.passport_date.data = member.passport_date_issued
        form.ethnicity_info.data = member.ethnicity_info
        form.teaching_research.data = member.teaching_research
        form.publication_promos.data = member.publication_promos
        form.social_media.data = member.social_media
        form.gown_size.data = member.gown_size
        form.hat_size.data = member.hat_size
        form.total_hours.data = member.total
        form.status.data = member.status
        return render_template("edit_member.html", date=date, name=session['name'], form=form, hour_result=hour_result)


@app.route("/add_member", methods=['POST', 'GET'])
@login_required
def add_member():
    form = member_info.MemberInfoForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            schoolArray = []
            cur = getCursor()
            cur.execute(f"select school_name from schools;")
            for row in cur.fetchall():
                schoolArray.append(str(row.school_name))
                school_name = form.school_name.data
            if form.school_name.data in schoolArray:  # the new school cannot be added if its not in the school list
                cur.execute(
                    f"select school_id from schools where school_name='{school_name}';")
                result = cur.fetchall()
                school_id = result[0]
                print(school_id)
                upsertMember(form, 'new', school_id)
                message = 'You have successfully added a new student.'
                return render_template('add_member.html', name=session['name'], form=form, message=message)
            else:
                print(form.errors)
                return render_template('add_member.html', name=session['name'], form=form)
        else:
            print(form.errors)
            return render_template('add_member.html', name=session['name'], form=form)
    else:
        return render_template("add_member.html", name=session['name'], form=form)


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
            mem.insert(25, coor[-1])  # insert cut-off date for the data
            member = uploads.mem_obj(mem)
            member.insert_db(events)
        return redirect(url_for('member'))
    #  read uploaded excel file and send info to client-side
    else:
        excelpath = upload_path('file')
        try:
            df_list = uploads.get_mem_df(excelpath)
            df_member = df_list[0]
            df_coor = df_list[1]
            mem_col = df_member.columns
            mem_data = df_member.values
            coor_col = df_coor.columns
            coor_data = df_coor.values
        except Exception as e:
            return render_template('error.html', name=session['name'])
        return render_template('member_upload.html', mem_col=mem_col, mem_data=mem_data,
                               coor_col=coor_col, coor_data=coor_data, name=session['name'])


@app.route("/school", methods=['POST', 'GET'])
@login_required
def school():
    cur = db.getCursor()
    sch_criteria_dict = filter_info.sch_criteria_dict
    filter_criteria = filter_info.get_criteria(sch_criteria_dict)
    if request.method == 'POST':
        sql = filter_info.get_sql(
            'school_details', 'school_id', sch_criteria_dict)
    else:
        sql = "SELECT * FROM school_details ORDER BY school_id;"
    cur.execute(sql)
    results = cur.fetchall()
    school_list = filter_info.get_display_list(results, schools_info.school)
    return render_template('school.html', name=session['name'], schoollist=school_list, schoolcriteria=filter_criteria)


@app.route("/school_upload", methods=['POST'])
@login_required
def school_upload():
    form = request.form
    # get data from client-side and insert into database
    if form:
        for i in range(0, len(form)-1):
            school_info = request.form.getlist(f'school{i}')
            test(school_info[17])
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
            return render_template('error.html')
        return render_template('school_upload.html', cols=school_cols, data=school_data, name=session['name'])


@app.route("/edit_school", methods=['POST', 'GET'])
@login_required
def edit_school():
    cur = getCursor()
    school_id = request.args.get('id')
    form = schools_info.SchoolInfoForm()
    cur.execute(f"select * from schools_info where school_id={school_id};")
    member = cur.fetchone()
    if request.method == 'POST':
        if form.validate_on_submit():
            upsertMember(form, school_id)
            return render_template('edit_member.html', name=session['name'], form=form)
        else:
            print(form.errors)
            return render_template('edit_member.html', name=session['name'], form=form)
    else:
        form.first_name.data = member.first_name
        form.last_name.data = member.last_name
        form.school_name.data = member.school_name
        form.username.data = member.username
        form.gender.data = member.gender
        form.ethnicity.data = member.ethnicity
        form.age.data = member.member_age
        form.password.data = member.password
        form.continuing_new.data = member.continuing_new
        form.previous_hours.data = member.previous
        form.passport_number.data = member.passport_number
        form.passport_date.data = member.passport_date_issued
        form.ethnicity_info.data = member.ethnicity_info
        form.teaching_research.data = member.teaching_research
        form.publication_promos.data = member.publication_promos
        form.social_media.data = member.social_media
        form.gown_size.data = member.gown_size
        form.hat_size.data = member.hat_size
        form.total_hours.data = member.total
        form.status.data = member.status
        return render_template("edit_member.html", date=date, name=session['name'], form=form)


@app.route("/destination", methods=['POST', 'GET'])
@login_required
def destination():
    cur = db.getCursor()
    destination_criteria_dict = filter_info.destination_criteria_dict
    filter_criteria = filter_info.get_criteria(destination_criteria_dict)
    if request.method == 'POST':
        sql = filter_info.get_sql('destinations', 'ld_id', destination_criteria_dict)
        cur.execute(sql)
        dest_list=cur.fetchall()
        return render_template('destination.html', name=session['name'], dest_list=dest_list, criteria=filter_criteria)
    else:
        cur.execute("SELECT * FROM destinations ORDER BY ld_id;")
        dests = cur.fetchall()
        return render_template('destination.html', dests=dests, name=session['name'], criteria=filter_criteria)


@app.route("/edit_destination", methods=['POST', 'GET'], endpoint='1')
@app.route("/add_destination", methods=['POST', 'GET'], endpoint='2')
@login_required
def edit_destination():
    version = request.endpoint
    cur = getCursor()
    form = destinations.DestinationForm()
    ld_id = request.args.get('id')
    if request.method == 'POST':
        if form.validate_on_submit():
            if version == '1':
                upsertDestinations(form, ld_id)
                message = 'Update successful'
                return render_template('edit_destination.html', name=session['name'], form=form, message=message)
            else:
                upsertDestinations(form, 'new')
                message = 'You have successfully added a new learning destination.'
                return render_template('add_destination.html', name=session['name'], form=form, message=message)
        else:
            print(form.errors)
            if version == '1':
                return render_template('edit_destination.html', name=session['name'], form=form)
            else:
                return render_template('add_destination.html', name=session['name'], form=form)
    else:
        if version == '1':
            cur.execute(f"select * from destinations where ld_id={ld_id};")
            ld = cur.fetchone()
            form.status.data = ld.status
            form.ld_name.data = ld.ld_name
            form.contact_person.data = ld.contact_person
            form.ld_position.data = ld.ld_position
            form.address.data = ld.address
            form.region.data = ld.region
            form.postal_address.data = ld.postal_address
            form.email.data = ld.email
            form.phone_number.data = ld.phone_number
            form.web_address.data = ld.web_address
            form.member_cost.data = ld.member_cost
            form.adult_cost.data = ld.adult_cost
            form.agrt_signed.data = ld.agrt_signed
            form.rov_signed.data = ld.rov_signed
            form.poster_sent.data = ld.poster_sent
            form.logo_sent.data = ld. logo_sent
            form.promo.data = ld.promo
            form.photo.data = ld.photo
            form.note.date = ld.note
            return render_template('edit_destination.html', form=form, name=session['name'])
        else:
            return render_template('add_destination.html', name=session['name'], form=form)


@app.route("/destination_upload", methods=['POST'])
@login_required
def destination_upload():
    form = request.form
    # get data from client-side and insert into database
    if form:
        paperwork = request.form.getlist('des_col')[20:-1]
        print(paperwork, 'ppppppppppppppppppppppppp')
        for i in range(0, len(form)-1):
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
            dest_cols = df_dest.columns
            dest_data = df_dest.values

        except Exception as e:
            return render_template('error.html')
        return render_template('destination_upload.html', cols=dest_cols, data=dest_data, name=session['name'])


@app.route("/volunteer", methods=['POST', 'GET'])
@login_required
def volunteer():
    cur = db.getCursor()
    volun_criteria_dict = filter_info.volun_criteria_dict
    filter_criteria = filter_info.get_criteria(volun_criteria_dict)
    print(filter_criteria)
    if request.method == 'POST':
        sql = filter_info.get_sql(
            'volun_detail', 'volun_id', volun_criteria_dict)
    else:
        sql = "SELECT * FROM volun_detail ORDER BY volun_id;"
    cur.execute(sql)
    results = cur.fetchall()
    volun_list = filter_info.get_display_list(results, classes.volunteer)
    return render_template('volunteer.html', name=session['name'], voluns=volun_list, criteria=filter_criteria)


@app.route("/volunteer_upload", methods=['POST', 'GET'])
@login_required
def volunteer_upload():
    form = request.form
    # get data from client-side and insert into database
    if form:
        events = request.form.getlist('col')[38:-1]
        for i in range(0, len(form)-1):
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
            return render_template('error.html')
        return render_template('volunteer_upload.html', cols=volun_cols, data=volun_data, name=session['name'])


@app.route("/event", methods=['POST', 'GET'])
@login_required
def event():
    cur = db.getCursor()
    cur.execute("SELECT events.*, event_attend.number,volun_attend.attend FROM events\
        LEFT JOIN event_attend ON events.event_id = event_attend.event_id LEFT JOIN \
        volun_attend ON events.event_id = volun_attend.event_id ORDER BY events.event_date DESC;")
    events = cur.fetchall()
    print(events, 'eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
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
@admin_access
def users():
    cur = db.getCursor()
    cur.execute("SELECT admin.user_id, admin.first_name, admin.surname, admin.phone_number, admin.email, \
        authorisation.user_access, admin.status FROM admin JOIN authorisation ON admin.user_id=authorisation.user_id \
        ORDER BY surname;")
    select_result = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    return render_template('users.html', users=select_result, dbcols=column_names, name=session['name'])


@app.route("/edit_user", methods=['POST', 'GET'])
@login_required
@admin_access
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
        cur.execute("SELECT admin.user_id, admin.first_name, admin.surname, admin.phone_number, admin.email, \
            authorisation.user_access, admin.status FROM admin JOIN authorisation ON admin.user_id=authorisation.user_id \
             WHERE admin.user_id = %s;", (user_id,))
        userinfo = cur.fetchone()
        return render_template("edit_user.html", userinfo=userinfo, name=session['name'])


@app.route("/add_user", methods=['POST', 'GET'])
@login_required
@admin_access
def add_user():
    if request.method == 'POST':
        user_id = genID()
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        user_access = request.form.get('user_access')
        status = "active"
        cur = db.getCursor()
        cur.execute("INSERT INTO admin(user_id, first_name, surname, phone_number, email, status) VALUES (%s,%s,%s,%s,%s,%s);",
                    (int(user_id), first_name, surname, phone_number, email, status,))
        cur.execute(
            "INSERT INTO authorisation(user_id, username, user_access) VALUES (%s,%s,%s);", (user_id, email, user_access))
        flash(f'User successfully added!', 'success')
        return redirect(url_for('users'))
    return render_template('add_user.html', name=session['name'])


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
    # generating excel of blanck template and send to client-side
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
                f'{app.root_path}\downloads\Completed.zip', 'w')
            for schoolid in school_list:

                filename = spreadsheet.gen_mem_comp(schoolid)
                zfile.write(filename)
            zfile.close()
            return send_file(f'{app.root_path}\downloads\Completed.zip',
                             mimetype='zip',
                             attachment_filename='Completed.zip',
                             as_attachment=True)
    return render_template('download_mem_sheet.html', schools=schools, name=session['name'])


@app.route("/download_dest_sheet", methods=['POST', 'GET'])
@login_required
@no_cache
def download_dest_sheet():
    file = spreadsheet.gen_dest_sheet()
    return send_file(file, mimetype='xlsx', as_attachment=True)


@app.route("/download_volun_sheet", methods=['POST', 'GET'])
@login_required
@no_cache
def download_volun_sheet():
    file = spreadsheet.gen_volun_sheet()
    return send_file(file, mimetype='xlsx', as_attachment=True)


@app.route("/download_school_sheet", methods=['POST', 'GET'])
@login_required
@no_cache
def download_school_sheet():
    sheet = request.args.get('sheet')
    file =  spreadsheet.gen_sch_sheet(sheet)
    return send_file(file, mimetype = 'xlsx', as_attachment=True)





if __name__ == '__main__':
    app.run(debug=True)
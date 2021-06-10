import db, app
import pandas as pd
import getid
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, TextAreaField, IntegerField
from wtforms import validators
from wtforms.fields.html5 import EmailField, DateField, TelField
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields.html5 import TimeField
from datetime import datetime, timedelta
from wtforms.fields.simple import TextAreaField, TextField


class school:
    def __init__(self,l=[]):
        self.id = int(l[0])
        self.name = l[1]
        self.who = l[2]
        self.council = l[3]
        self.category = l[4]
        self.status = l[5]
        # self.coor_id = int(l[6])
        self.coor_name = l[6]
        self.coor_email = l[7]
        self.training = l[8] 
        self.launch = l[9] 
        self.presentation = l[10] 
        self.portal = l[11]
        self.passports = l[12]
        self.agreement = l[13]
        self.consent = l[14]
        self.notes = l[15]

        self.year = int(l[16])
        self.returning = int(l[17])
        self.max = int(l[18])
        self.request = int(l[19])
        self.confirm = int(l[20])

    def insert_db(self):
        cur = db.getCursor()
        cur.execute("UPDATE schools SET school_name = %s, who = %s, council = %s, category = %s, \
            status = %s,  training = %s, launch = %s, presentation = %s, portal = %s, \
            passports = %s, agreement = %s, consent = %s, notes = %s WHERE school_id = %s;", (self.name, self.who,
                                                                                              self.council, self.category, self.status, self.training, self.launch, self.presentation,
                                                                                              self.portal, self.passports, self.agreement, self.consent, self.notes, self.id,))
        sql = "INSERT INTO coordinator(school_id, name, email) VALUES(%s, '%s', '%s') ON CONFLICT \
        (school_id) DO UPDATE SET school_id = EXCLUDED.school_id, name = EXCLUDED.name, \
        email = EXCLUDED.email;" % (self.id, self.coor_name, self.coor_email)
        cur.execute(sql)
        # cur.execute("UPDATE coordinator SET name = %s, email = %s WHERE school_id = %s;",( self.coor_name,self.coor_email,self.id))
        sql = f"INSERT INTO school_members(school_id, year, return_no ,max_no, request_no, confirm_no) VALUES({self.id}, \
            '{self.year}',{self.returning}, {self.max},{self.request},{self.confirm}) ON CONFLICT (school_id, year) DO UPDATE \
            SET school_id = EXCLUDED.school_id, year = EXCLUDED.year, return_no = EXCLUDED.return_no, \
            max_no =EXCLUDED.max_no, request_no = EXCLUDED.request_no, confirm_no = EXCLUDED.confirm_no;"
        cur.execute(sql)
        # sql = f" INSERT INTO school_members (school_id, year, return_no) VALUES ({self.id}, {self.year-1}, \
        #     {self.returning}) ON CONFLICT (school_id, year) DO UPDATE SET school_id =EXCLUDED.school_id, \
        #     year = EXCLUDED.year, return_no = EXCLUDED.return_no ;"
        # cur.execute(sql)


def school_obj(l=[]):
    school_obj = school(l)
    school_name = school_obj.name
    school_obj.id = getid.get_schoolid(school_name)
    return school_obj


def get_df(excelpath):
    typedict = {
        'Total(Last Year)' : str,
        'Returning (Last year)'	: str,
        'Max Number(Current Year)'	: str,
        'Requested Number(Current Year)' : str,	
        'Confirmed Number(Current Year)' : str

    }
    df_school = pd.read_excel(excelpath,0,dtype=typedict)
    df_school.update(df_school.iloc[:,17:].fillna(0))
    df_school.update(df_school.iloc[:,[8,9,10]].fillna('NA'))
    df_school.fillna('', inplace=True)
    df_school.loc[:, 'index'] = df_school.index

    return df_school


def active_schools_count():
    # Function returns the number of active schools in the system to display on dashboard
    parameters = [app.current_year()]
    query = "SELECT COUNT(schools.status) FROM schools JOIN school_members ON schools.school_id=school_members.school_id \
        WHERE schools.status='active' OR schools.status='Active' and school_members.year=%s;"
    result = db.getOne(query, parameters)
    return result[0]


def in_progress_schools_count():
    # Function returns the number of in progress schools in the system to display on dashboard
    parameters = [app.current_year()]
    query = "SELECT COUNT(schools.status) FROM schools JOIN school_members ON schools.school_id=school_members.school_id \
        WHERE schools.status='in progress' OR schools.status='In Progress' and school_members.year=%s;"
    result = db.getOne(query, parameters)
    return result[0]


def total_schools_count():
    # Function returns the total number of schools in the system to display on dashboard
    parameters = [app.current_year()]
    query = "SELECT COUNT(school_id) FROM school_members WHERE year=%s;"
    result = db.getOne(query, parameters)
    return result[0]


class SchoolInfoForm(FlaskForm):
    school_name = StringField(label='School Name')

    who = StringField(label='Who')

    council = StringField(label='Council')

    category = StringField(label='Category')

    status = SelectField(label='Status', choices=['Active', 'Deative'])

    training = StringField(label='Training')

    launch = StringField(label='Launch')

    presentation = StringField(label='Presentation')

    portal = SelectField(label='portal', choices=['Y', 'N'])

    passports = SelectField(label='Passports', choices=['Y', 'N'])

    agreement = SelectField(label='Agreement', choices=['Y', 'N'])
        

    consent = SelectField(label='Consent', choices=['Y', 'N'])


    notes = TextField (label='Note ')

    name = StringField(label='name')

    email = StringField(label='email')
    
    confirm = StringField(label='confirm')

    submit = SubmitField(label=('Save'))
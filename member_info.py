from schools_info import school
from flask.app import Flask
import db, app
import pandas as pd
import getid
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms import validators
from wtforms.fields.html5 import DateField
from wtforms.fields.simple import TextField

class members:
    def __init__(self,l=[]):
        self.id = int(l[0]) if l[0] != '' else 1
        self.first = l[1]
        self.last = l[2]
        self.gender = l[3]
        self.age = int(l[4]) if l[4] != '' else None 
        self.ethnicity = l[5]
        self.mtype = l[6]

        self.status = l[7]
        self.passport = l[8] 
        
        self.date = l[9]
        self.eth_info = l[10]
        self.research = l[11]
        self.promos = l[12]
        self.social = l[13]

        self.username = l[14]
        self.password = l[15]
        self.school = l[16].lower()

        self.previous = float(l[17])
        self.term1 = float(l[18])
        self.term2 = float(l[19])
        self.term3 = float(l[20])
        self.term4 = float(l[21])
        self.total = float(l[22])
        self.gown = l[23]
        self.hat = l[24]
        self.year = int(l[25][0:4])

        self.attend = l[26:-1] if len(l)>27 else False


    def insert_db(self,events=[]):
        print(self.previous, 'sssssssssssssssssssssssssssssssssssssssssss')
        cur = db.getCursor()
        cur.execute("UPDATE members SET school_id = %s, first_name = %s, last_name = %s, username=%s, \
            password=%s, gender=%s, member_age=%s, ethnicity=%s, continuing_new = %s, \
             passport_number=%s, passport_date_issued=%s, ethnicity_info=%s, teaching_research=%s, \
             publication_promos=%s, social_media=%s, gown_size=%s, hat_size=%s, status = %s WHERE \
             member_id = %s;",(self.school, self.first, self.last, self.username, self.password, self.gender, 
            self.age,self.ethnicity,self.mtype, self.passport, self.date, self.eth_info, self.research, self.promos, 
            self.social,  self.gown, self.hat, self.status,self.id,))
        
        sql = f"INSERT INTO membershours VALUES({self.id}, '{self.year}', {self.term1}, {self.term2}, \
             {self.term3}, {self.term4}) ON CONFLICT (member_id, year) DO UPDATE SET member_id = EXCLUDED.member_id, \
            year = EXCLUDED.year, term1 = EXCLUDED.term1, term2 = EXCLUDED.term2, term3 = EXCLUDED. term3, term4 = EXCLUDED.term4;"
        cur.execute(sql)

        cur.execute("UPDATE membershours SET total = (SELECT SUM(term4) FROM membershours WHERE member_id = %s) \
            WHERE member_id = %s AND year = %s;",(self.id,self.id,self.year))

        
        if events:
            for i in range(0,len(events)):
                sql = "INSERT INTO attendance VALUES(%s, %s,'%s') ON CONFLICT (member_id, event_id) \
                DO UPDATE SET member_id = EXCLUDED.member_id, event_id = EXCLUDED.event_id,status = \
                EXCLUDED.status" %(self.id,events[i],self.attend[i].lower())
                cur.execute(sql)


def active_members_count():
    # Function returns the number of active schools in the system to display on dashboard
    parameters = [app.current_year()]
    query = "SELECT COUNT(members.member_id) FROM members JOIN membershours ON members.member_id=membershours.member_id \
        WHERE status='active' OR status='Active' AND year='%s';"
    result = db.getOne(query, parameters)
    return result[0]

def total_members_hours():
    # Function returns the number of active schools in the system to display on dashboard
    parameters = [app.current_year()]
    query = "SELECT SUM(total) FROM mem_hour_detail WHERE year=%s;"
    result = db.getOne(query, parameters)
    return result[0]
    

class MemberInfoForm(FlaskForm):
    school_name = StringField(label='School Name ', validators=[
        validators.regexp('^[a-zA-Z ]*$', message='The school should in the list')])

    first_name = StringField(label='First Name *', validators=[
        validators.DataRequired(),
        validators.regexp('^\w+$', message='Letters only')
    ])
    last_name = StringField(label='Last Name *', validators=[
        validators.DataRequired(),
        validators.regexp('^\w+$', message='Letters only')
    ])
    username = StringField(label='Username ', validators=[
        validators.regexp('^\w+$', message='Letters only')
    ])
    password = StringField(label='Password ', validators=[
        validators.regexp('^\w+$', message='Letters only')
    ])
    gender = SelectField(label='Gender ', choices=['Boy', 'Girl', 'Other'])
 
    age = IntegerField(label='Age ')

    ethnicity = StringField(label='Ethnicity ')

    continuing_new = SelectField(label='Continuing or New ', choices=['Continuing', 'New'])

    passport_number = StringField(label='Passport Number ')

    previous_hours = StringField(label='Previous Hours ')

    passport_date = StringField(label='Passport Date Issued ')

    ethnicity_info = SelectField(label='Ethnicity Info ', choices=['True', 'False'])

    teaching_research = SelectField(label='Teaching Research ', choices=['True', 'False'])

    publication_promos = SelectField(label='Pubilication Promos ', choices=['True', 'False'])

    social_media = SelectField(label='Social Media ', choices=['True', 'False'])
    
    gown_size = SelectField(label='Gown Size ', choices=['','S', 'M', 'L'])

    hat_size = SelectField(label='Hat Size ', choices=['','S', 'M', 'L'])  

    status = SelectField(label='Status *', validators=[
        validators.DataRequired(),
    ], choices=['Active', 'Deactive'])
    submit = SubmitField(label=('Submit'))





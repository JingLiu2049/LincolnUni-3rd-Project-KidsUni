import db
import pandas as pd
import getid
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms import validators
from wtforms.fields.html5 import DateField


def active_members_count():
    # Function returns the number of active schools in the system to display on dashboard
    query = "SELECT COUNT(member_id) FROM members;"
    result = db.getOne(query, [])
    return result[0]

def total_members_hours():
    # Function returns the number of active schools in the system to display on dashboard
    query = "SELECT SUM(total) FROM members;"
    result = db.getOne(query, [])
    return result[0]
    

class MemberInfoForm(FlaskForm):
    school_name = StringField(label='School Name *', validators=[
        validators.DataRequired(), validators.regexp('^[a-zA-Z ]*$', message='The school should in the list')])

    first_name = StringField(label='First Name *', validators=[
        validators.DataRequired(),
        validators.regexp('^\w+$', message='Letters only')
    ])
    last_name = StringField(label='Last Name *', validators=[
        validators.DataRequired(),
        validators.regexp('^\w+$', message='Letters only')
    ])
    username = StringField(label='Username *', validators=[
        validators.DataRequired(),
        validators.regexp('^\w+$', message='Letters only')
    ])
    password = StringField(label='Password *', validators=[
        validators.DataRequired(),
        validators.regexp('^\w+$', message='Letters only')
    ])
    gender = SelectField(label='Gender * ', validators=[
        validators.DataRequired(),], choices=['Boy', 'Girl', 'Other'])
 
    age = IntegerField(label='Age *', validators=[
        validators.DataRequired()]
    )

    ethnicity = StringField(label='Ethnicity *', validators=[
        validators.DataRequired(),        
    ])

    continuing_new = SelectField(label='Continuing or New', validators=[
        validators.DataRequired(),], choices=['Continuing', 'New'])

    passport_number = StringField(label='Passport Number*', validators=[
        validators.DataRequired(),
    ])

    previous_hours = StringField(label='Previous Hours *', validators=[
        validators.DataRequired()]
    )

    passport_date = DateField(label='Passport Date Issued *', validators=[
        validators.DataRequired(),
    ])

    ethnicity_info = SelectField(label='Ethnicity Info *', validators=[
        validators.DataRequired(),
    ], choices=['True', 'False'])

    teaching_research = SelectField(label='Teaching Research *', validators=[
        validators.DataRequired(),
    ], choices=['True', 'False'])

    publication_promos = SelectField(label='Pubilication Promos *', validators=[
        validators.DataRequired(),
    ], choices=['True', 'False'])

    social_media = SelectField(label='Social Media *', validators=[
        validators.DataRequired(),
    ], choices=['True', 'False'])

    total_hours = StringField(label='Total Hours *',validators=[
        validators.DataRequired(),
    ])
    
    gown_size = SelectField(label='Gown Size ', choices=['','S', 'M', 'L'])

    hat_size = SelectField(label='Hat Size ', choices=['','S', 'M', 'L'])  

    status = SelectField(label='Status *', validators=[
        validators.DataRequired(),
    ], choices=['Active', 'Deactive'])
    submit = SubmitField(label=('Save'))
from wtforms.fields.simple import TextAreaField, TextField
import db
import pandas as pd
import getid
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField ,TextAreaField
from wtforms import validators
from wtforms.fields.html5 import DateField, EmailField, TelField, URLField
import email_validator

def active_destinations_count():
    # Function returns the number of active learning destinations in the system to display on dashboard
    query = "SELECT COUNT(status) FROM destinations WHERE status='active' OR status='Active';"
    result = db.getOne(query, [])
    return result[0]

def pending_destinations_count():
    # Function returns the number of pending learning destinations in the system to display on dashboard
    query = "SELECT COUNT(status) FROM destinations WHERE status='pending' OR status='Pending';"
    result = db.getOne(query, [])
    return result[0]

def total_destinations_count():
    # Function returns the total number of learning destinations in the system to display on dashboard
    query = "SELECT COUNT(ld_id) FROM destinations;"
    result = db.getOne(query, [])
    return result[0]


class DestinationForm(FlaskForm):
    status = StringField(label='Status *', validators=[
        validators.DataRequired(), validators.regexp('^\w+$', message='Letters only')])

    ld_name = StringField(label='Name *', validators=[
        validators.DataRequired(),
        validators.regexp('^[a-zA-Z ]*$', message='Letters only')
    ])
    contact_person = StringField(label='Contact Person*', validators=[
        validators.DataRequired(),
        validators.regexp('^[a-zA-Z ]*$', message='Letters only')
    ])

    ld_position = StringField(label='Position ', validators=[
        validators.DataRequired(),
        validators.regexp('^[a-zA-Z ]*$', message='Letters only')
    ])

    address = StringField(label='Address *', validators=[
        validators.DataRequired()])

    region = StringField(label='Region *', validators=[
        validators.DataRequired(), 
        validators.regexp('^[a-zA-Z ]*$', message='Letters only')])
 
    postal_address = StringField(label='Postal Address *', validators=[
        validators.DataRequired()])

    phone_number = TelField(label='Phone Number *', validators=[
        validators.DataRequired(),        
    ])

    email = EmailField(label='Email *', validators=[
        validators.DataRequired(), validators.Email()])

    web_address = URLField(label='Web Address *', validators=[
        validators.DataRequired(),
    ])

    member_cost = StringField(label='Member Cost ')

    adult_cost = StringField(label='Adult Cost ')

    agrt_signed = DateField(label='Agreement Signed *', validators=[
        validators.DataRequired(),
    ])

    rov_signed = DateField(label='ROV Signed *', validators=[
        validators.DataRequired()])

    poster_sent = SelectField(label='Poster Sent *', validators=[
        validators.DataRequired(),
    ], choices=['','Yes', 'No'])

    logo_sent = SelectField(label='Logo Sent *', validators=[
        validators.DataRequired(),
    ], choices=['','Yes', 'No'])

    promo = SelectField(label='Promotion *', validators=[
        validators.DataRequired(),
    ], choices=['','Yes', 'No'])

    note = TextField (label='Note Facebook Promotion ')
    
    photo = SelectField(label='Promotion ', choices=['Yes', 'No'])

    submit = SubmitField(label=('Save'))
from wtforms.fields.simple import TextAreaField, TextField
import db
import pandas as pd
import getid
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField ,TextAreaField
from wtforms import validators
from wtforms.fields.html5 import DateField, EmailField, TelField, URLField
import email_validator

class destination:
    def __init__(self,l=[]):
        self.id = int(l[0]) if l[0] != '' else 1
        self.status = l[1]
        self.name = l[2]
        self.contact = l[3]
        self.ld_position = l[4]
        self.address = l[5]
        self.region = l[6] 
        self.post = l[7]
        self.phone = l[8]
        self.email = l[9]
        self.web = l[10]
        self.cost = l[11]
        self.adult_cost = l[12]
        self.agreement = l[13] if l[13] != '' else None
        self.rov = l[14] if l[14] != '' else None
        self.poster = l[15]
        self.logo = l[16]
        self.promo = l[17]
        self.photo = l[18]
        self.note = l[19]

        
        self.paperwork = l[20:] if len(l)>20 else False
    # Function in each class to insert data into database
    def insert_db(self,paperwork):
        cur = db.getCursor()
        cur.execute("UPDATE destinations SET status = %s, ld_name = %s, contact_person = %s, ld_position = %s, \
            address = %s, region = %s, postal_address = %s, phone_number = %s,email = %s, web_address = %s, \
            member_cost = %s, adult_cost = %s, agrt_signed = %s, rov_signed = %s, poster_sent = %s, logo_sent = %s, \
            promo = %s, photo = %s, note = %s WHERE ld_id = %s;",(self.status, self.name, self.contact, self.ld_position, self.address,
            self.region, self.post, self.phone, self.email, self.web, self.cost, self.adult_cost, self.agreement, self.rov,
            self.poster, self.logo, self.promo, self.photo, self.note, self.id, ))
        if paperwork:
            for i in range(0,len(paperwork)):
                sql = "INSERT INTO paperwork VALUES(%s, '%s','%s') ON CONFLICT (ld_id, year) \
                DO UPDATE SET ld_id = EXCLUDED.ld_id, year = EXCLUDED.year, status = \
                EXCLUDED.status" %(self.id,f'{paperwork[i]}-12-31',self.paperwork[i])
                cur.execute(sql)

    # def __del__(self):
    #     print('dest obj has been delated',self)

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
    status = SelectField(label='Status *', validators=[
        validators.DataRequired()],  choices=['Active', 'Deactive','In Progress'])

    ld_name = StringField(label='Name *', validators=[
        validators.DataRequired()
    ])
    contact_person = StringField(label='Contact Person', validators=[
        validators.regexp('^[a-zA-Z ]*$', message='Letters only')
    ])

    ld_position = StringField(label='Position ', validators=[
        validators.regexp('^[a-zA-Z ]*$', message='Letters only')
    ])

    address = StringField(label='Address ')

    region = StringField(label='Region ')

    postal_address = StringField(label='Postal Address ')

    phone_number = TelField(label='Phone Number ')

    email = EmailField(label='Email ')

    web_address = URLField(label='Web Address ')

    member_cost = StringField(label='Member Cost ')

    adult_cost = StringField(label='Adult Cost ')

    agrt_signed = StringField(label='Agreement Signed ')

    rov_signed = StringField(label='ROV Signed ')

    poster_sent = SelectField(label='Poster Sent ', choices=['','Yes', 'No'])

    logo_sent = SelectField(label='Logo Sent' , choices=['','Yes', 'No'])

    promo = SelectField(label='Facebook Promotion ', choices=['','Yes', 'No'])

    note = TextField (label='Note ')

    photo = SelectField(label='Photo Provide ', choices=['','Yes', 'No'])

    submit = SubmitField(label=('Submit'))

# if ld_id is not new, update destiantion daata for sql, otherwise insert a new destiantion
# get data from destiantion form
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
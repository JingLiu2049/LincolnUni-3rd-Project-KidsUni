import db
import pandas as pd
import getid

class learning_destination:
    def __init__(self,l=[]):
        self.id = int(l[0])
        self.status = l[1]
        self.name = l[2]
        self.contact_person = l[3]
        self.position = l[4]
        self.address = l[5]
        self.region = l[6] 
        self.postal_address = l[7]
        self.phone_number = l[8]
        self.email = l[9]
        self.web_address = l[10]
        self.member_cost = l[11]
        self.adult_cost = l[12]
        self.agrt_signed = l[13]
        self.rov_signed = l[14]
        self.poster_sent = l[15]
        self.logo_sent = l[16]
        self.promo = l[17]
        self.photo = l[18]
        self.note = l[19]

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
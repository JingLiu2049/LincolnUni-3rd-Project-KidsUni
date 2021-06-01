import db
import pandas as pd
import getid


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
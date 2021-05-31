import db
import pandas as pd
import getid


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
    


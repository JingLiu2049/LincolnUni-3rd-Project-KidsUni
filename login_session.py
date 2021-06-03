from flask import session
import db
import classes

def perform_login(username, password):
    query = "SELECT user_id, user_access FROM authorisation WHERE username=%s AND password =%s"
    result = db.getOne(query,[username,password])
    if result == None:
        return False
    session['loggedin'] = True
    session['user_id'] = result[0]
    if result[1] == "admin":
        session['user_access'] = "admin"
        session['name'] = classes.user.first_name
        return True
    if result[1] == "restricted":
        session['user_access'] = "restricted"
        session['name'] = classes.user.first_name
        return True

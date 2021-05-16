import db

def get_memid():
    cur = db.getCursor()
    cur.execute("INSERT INTO members(member_id) VALUES (nextval('membered_seq')) RETURNING member_id;")
    memberid = cur.fetchone()[0]
    return memberid

def get_schoolid(school_name):
    cur = db.getCursor()
    cur.execute("SELECT school_id FROM schools where school_name = %s;",(school_name.lower(),))
    result = cur.fetchone()
    if result:
        school_id = result[0]
    else:
        cur.execute("INSERT INTO schools(school_id,school_name) VALUES (nextval('schoolid_seq'),%s) RETURNING school_id;",(school_name.lower(),))
        school_id  = cur.fetchone()[0]
    return int(school_id)


def get_event_id():
    cur = db.getCursor()
    cur.execute("INSERT INTO events_id) VALUES (nextval('eventid_seq')) RETURNING event_id;")
    eventid = cur.fetchone()[0]
    return eventid
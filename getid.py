import db



def get_memid():
    cur = db.getCursor()
    cur.execute("INSERT INTO members(member_id) VALUES (nextval('membered_seq')) RETURNING member_id;")
    memberid = int(cur.fetchone()[0])
    return memberid

def get_schoolid(school_name):
    cur = db.getCursor()
    name = school_name.lower()
    cur.execute("SELECT school_id FROM schools where school_name = %s;",(name,))
    result = cur.fetchone()
    if result:
        school_id = result[0]
    else:
        cur.execute("INSERT INTO schools(school_id,school_name) VALUES (nextval('schoolid_seq'),%s) RETURNING school_id;",(name,))
        school_id  = cur.fetchone()[0]
    return int(school_id)


def get_event_id():
    cur = db.getCursor()
    cur.execute("INSERT INTO events(event_id) VALUES (nextval('eventid_seq')) RETURNING event_id;")
    eventid = int(cur.fetchone()[0])
    return eventid

def get_dest_id():
    cur = db.getCursor()
    cur.execute("INSERT INTO destinations(ld_id) VALUES (nextval('destinationid_seq')) RETURNING ld_id;")
    dest_id =  int(cur.fetchone()[0])
    return dest_id

def get_volun_id():
    cur = db.getCursor()
    cur.execute("INSERT INTO volunteers(volun_id) VALUES (nextval('volunteerid_seq')) RETURNING volun_id;")
    volun_id =  int(cur.fetchone()[0])
    return volun_id


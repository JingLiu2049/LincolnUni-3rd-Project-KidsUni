import psycopg2
import connect
dbconn = None
def get_conn():
    conn = psycopg2.connect(connect.conn_string)
    return conn

def set_connect():    
    global dbconn    
    if dbconn == None or dbconn.closed == True:
        conn = get_conn()
        dbconn = conn.cursor()  
        conn.autocommit = True
        return dbconn
    else:
        return dbconn

    
def test_connect():
    try:
        cur = set_connect()
        cur.execute('SELECT 1')
        return True
    except psycopg2.OperationalError:
        return False
    
def getCursor():
    global dbconn
    if not test_connect():
        return set_connect()
    return dbconn
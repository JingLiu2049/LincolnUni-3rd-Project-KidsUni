import psycopg2
import connect


dbuser = "postgres"
dbpass = "comp639639" #"PUT YOUR PASSWORD HERE"
dbhost = "childrenuni.cpeubo3go4d3.us-east-1.rds.amazonaws.com" #"PUT YOUR AWS Connect String here"
dbport = "5432"
dbname = "cu"



conn_string = "host=" + dbhost + " port=" + dbport + " dbname=" + dbname + " user=" + dbuser + " password=" + dbpass
dbconn = None

def get_conn():
    conn = psycopg2.connect(conn_string)
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

def getOne(query, parameters):
    # Parameters: query (string), parameters (list)
    # Output: first result from the database based on the search criteria provided in the query string and parameters
    cur = getCursor()
    cur.execute(query, parameters)
    return cur.fetchone()
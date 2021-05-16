import psycopg2
import connect
dbconn = None
conn = psycopg2.connect(connect.conn_string)
def getCursor():    
    global dbconn    
    if dbconn == None:
        # conn = psycopg2.connect(connect.conn_string)
        dbconn = conn.cursor()  
        conn.autocommit = True
        return dbconn
    else:
        return dbconn


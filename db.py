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

def getOne(query, parameters):
    # Parameters: query (string), parameters (list)
    # Output: first result from the database based on the search criteria provided in the query string and parameters
    cur = getCursor()
    cur.execute(query, parameters)
    return cur.fetchone()
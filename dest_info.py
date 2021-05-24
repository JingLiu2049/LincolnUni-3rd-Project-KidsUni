import db
import pandas as pd
import getid

class destination:
    def __init__(self,l=[]):
        self.id = int(l[0])
        self.status = l[1]
        self.name = l[2]
        self.contact = l[3]
        self.position = l[4]
        self.address = l[5]
        self.region = l[6] 
        self.post = l[7]
        self.phone = l[8]
        self.email = l[9]
        self.web = l[10]
        self.cost = l[11]
        self.adult_cost = l[12]
        self.agreement = l[13]
        self.rov = l[14]
        self.poster = l[15]
        self.logo = l[16]
        self.promo = l[17]
        self.photo = l[18]
        self.note = l[19]

        
        self.paperwork = l[20:-1] if len(l)>20 else False
    def insert_db(self):
        cur = db.getCursor()
        sql = "UPDATE destinations SET status = '%s', ld_name = '%s', contact_person = '%s', position = '%s', \
            address = '%s', region = '%s', postal_address = '%s', phone_number = '%s',email = '%s', web_address = '%s', \
            member_cost = '%s', adult_cost = '%s', agrt_signed = '%s', rov_signed = '%s', poster_sent = '%s', logo_sent = '%s', \
            promo = '%s', photo = '%s', note = '%s' WHERE ld_id = %s;" %(self.status, self.name, self.contact, self.position, self.address,
            self.region, self.post, self.phone, self.email, self.web, self.cost, self.adult_cost, self.agreement, self.rov,
            self.poster, self.logo, self.promo, self.photo, self.note, self.id ) 
        cur.execute(sql)




def get_df(path):
    df_active = pd.read_excel(path,0)

def des_obj(l=[]):
    des_obj = destination(l)
    if int(des_obj.id)/10000 < 1:
        des_obj.id = getid.get_des_id()
    return des_obj

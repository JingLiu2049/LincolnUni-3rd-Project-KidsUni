import db
import pandas as pd
import getid

class school:
    def __init__(self,l=[]):
        self.id = int(l[0])
        self.name = l[1]
        self.who = l[2]
        self.council = l[3]
        self.category = l[4]
        self.status = l[5]
        self.returningnumber = l[6] 
        self.maxnumber2021 = l[7]
        self.confirmednumber = l[8]
        self.coordinatorid = l[9]
        self.training = l[10]
        self.launch = l[11]
        self.passportpresentation = l[12]
        self.portal = l[13]
        self.passports = l[14]
        self.agreement = l[15]
        self.consent = l[16]
        self.notes = l[17]
        self.total = l[18:-1] if len(l)>18 else False

    def insert_db(self):
        cur = db.getCursor()
        sql = "UPDATE schools SET school_name = '%s', who = '%s', council = '%s', category = '%s', \
            status = '%s', returning_number = '%s', max_num_2021 = '%s', confirmed_num = '%s',coordinator_id = '%s', training = '%s', \
            launch = '%s', passport_presentation = '%s', portal = '%s', passports = '%s', agreement = '%s', consent = '%s', \
            notes = '%s' WHERE school_id = %s;" %(self.name, self.who, self.council, self.category, self.status,
            self.returningnumber, self.maxnumber2021, self.confirmednumber,self.coordinatorid, self.training, self.launch, self.passportpresentation, self.portal, self.passports,self.agreement,
            self.consent, self.notes, self.id ) 
        cur.execute(sql)




def get_df(path):
    df_active = pd.read_excel(path,0)

def school_obj(l=[]):
    school_obj = school(l)
    if int(school_obj.id)/10000 < 1:
        school_obj.id = getid.get_schoolid()
    return school_obj

def get_df(excelpath):
    df_school = pd.read_excel(excelpath,0)
    df_school.fillna('',inplace=True)
    df_school.loc[:,'index'] = df_school.index
    return df_school
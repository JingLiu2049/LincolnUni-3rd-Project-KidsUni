import db
import pandas as pd
import openpyxl as op
import os
import datetime
import getid
from openpyxl import load_workbook




class members:
    def __init__(self,l=[]):
        self.id = l[0]
        self.first = l[1]
        self.last = l[2]
        self.gender = l[3]
        self.age = l[4]
        self.ethnicity = l[5]
        self.mtype = l[6]

        self.status = l[7]
        self.passport = l[8]
        
        self.date = l[9]
        self.eth_info = l[10]
        self.research = l[11]
        self.promos = l[12]
        self.social = l[13]

        self.username = l[14]
        self.password = l[15]
        self.school = l[16]

        self.previous = l[17]
        self.term1 = l[18]
        self.term2 = l[19]
        self.term3 = l[20]
        self.term4 = l[21]
        self.total = l[22]
        self.gown = l[23]
        self.hat = l[24]

        self.attend = l[25:-1] if len(l)>26 else False

    def insert_db(self,events=[]):
        cur = db.getCursor()
        sql = "UPDATE members SET school_id = %s, first_name = '%s', last_name = '%s', username='%s', \
            password='%s', gender='%s', member_age=%s, ethnicity='%s', continuing_new = '%s', \
            passport_number='%s', passport_date_issued='%s', ethnicity_info='%s', teaching_research='%s', \
            publication_promos='%s', social_media='%s', gown_size='%s', hat_size='%s', status = '%s' WHERE \
            member_id = %s;" %(int(self.school), self.first, self.last, self.username, self.password, self.gender, 
            self.age,self.ethnicity,self.mtype, self.passport, self.date, self.eth_info, self.research, self.promos, 
            self.social, self.gown, self.hat, self.status,int(self.id))
        cur.execute(sql)
        if events:
            for i in range(0,len(events)):
                sql = "INSERT INTO attendance VALUES(%s, %s,'%s') ON CONFLICT (member_id, event_id) \
                DO UPDATE SET member_id = EXCLUDED.member_id, status = EXCLUDED.status" %(int(self.id),events[i],self.attend[i])
                cur.execute(sql)


    
def mem_obj(l=[]):
    mem_obj = members(l)
    school_id = getid.get_schoolid(mem_obj.school)
    mem_obj.school = school_id
    if int(mem_obj.id)/100000 < 1:
        mem_obj.id = getid.get_memid()
    return mem_obj
# obj = mem_obj('aaaaaaaaaaaaaaaaaaaaaaaa')
# print(obj.school)

# use pandas to read excel file and get data
def get_df(excelpath):
    df_school = pd.read_excel(excelpath,0,header=None,nrows=4)
    df_school.dropna(axis='columns',how='all',inplace=True)
    df_school.fillna('', inplace=True)
    name = df_school.loc[0,3]
    df1 = pd.read_excel(excelpath,0,header=[5])
    df1.iloc[:,14].fillna('NA', inplace=True)
    df1.dropna(axis = 0, how='all', subset=['First Name','Last Name','Age'],inplace=True)
    df1.fillna('', inplace=True)
    df1.rename(columns={'#':'Memberid'},inplace = True)
    df2 = pd.read_excel(excelpath,1,header=[5])
    df1.insert(14,'USERNAME',df2['USERNAME'].values)
    df1.insert(15,'PASSWORD',df2['PASSWORD'].values)
    df1.insert(16,'School name',name)
    df1.loc[:,'index'] = df1.index
    df_coor = pd.read_excel(excelpath,1,header=[1],nrows=1)
    df_coor.dropna(axis='columns',how='all',inplace=True)
    df_coor.loc[:,'School'] = df_school.loc[0,3]
    df_coor.loc[:,'Email'] = df_school.loc[2,3]
    df_coor.loc[:,'Phone'] = df_school.loc[3,3]
    
    return [df1,df_coor]

#  insert info of coordinator into database
def insert_coor(l=[]):
    cur = db.getCursor()
    school_id = getid.get_schoolid(l[4])
    cur.execute("SELECT coordinator_id FROM coordinator WHERE name = %s AND school_id =%s;",(l[0],school_id,))
    result = cur.fetchone()
    if result:
        coor_id = result[0]
        sql = "UPDATE coordinator SET name = '%s',school_id =%s, email ='%s', phone_number \
            = '%s',username = '%s',password='%s' WHERE coordinator_id = %s; " %(l[0],school_id,
            l[5],l[6],l[2],l[3],int(coor_id))
    else:
        sql = "INSERT INTO coordinator values (nextval('coorid_seq'),%s,'%s',null,'%s','%s','%s','%s')" %(
            school_id,l[0],l[5],l[6],l[2],l[3])
    cur.execute(sql)


    


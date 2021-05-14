import db
import pandas as pd
import openpyxl as op
import os
import datetime




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

        self.event = l[25:-1] if len(l)>26 else False

    def insert_db(self):
        cur = db.getCursor()
        sql = "UPDATE members SET school_id = %s, first_name = '%s', last_name = '%s', username='%s', password='%s', \
            gender='%s', member_age=%s, ethnicity='%s', continuing_new = '%s', passport_number='%s', passport_date_issued='%s', ethnicity_info='%s', \
            teaching_research='%s', publication_promos='%s', social_media='%s', gown_size='%s', hat_size='%s' WHERE member_id = %s;\
            " %(int(self.school), self.first, self.last, self.username, self.password, self.gender, self.age,self.ethnicity,
            self.mtype, self.passport, self.date, self.eth_info, self.research, self.promos, self.social, self.gown, self.hat, int(self.id))
        cur.execute(sql)

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
# schid = get_schoolid('Example Primary School')
# print(schid)
    
def mem_obj(l=[]):
    mem_obj = members(l)
    school_id = get_schoolid(mem_obj.school)
    mem_obj.school = school_id
    if int(mem_obj.id)/100000 < 1:
        mem_obj.id = get_memid()
    return mem_obj
# obj = mem_obj('aaaaaaaaaaaaaaaaaaaaaaaa')
# print(obj.school)

def get_df(excelpath):
    df_school = pd.read_excel(excelpath,0,header=None,nrows=4)
    df_school.dropna(axis='columns',how='all',inplace=True)
    df_school.fillna('', inplace=True)
    name = df_school.loc[0,3]
    print(df_school)
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

def insert_coor(l=[]):
    cur = db.getCursor()
    school_id = get_schoolid(l[4])
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

def gen_endyear_temp(schoolid):
        cur = db.getCursor()
        basepath  = os.path.dirname(__file__)
        templatePath =os.path.join(basepath,'downloads','End year template.xlsx')
        cur.execute("SELECT school_name FROM schools WHERE school_id = %s;",(schoolid ,))
        sch_name = cur.fetchone()[0]
        filename = f'{datetime.datetime.now().year}_{sch_name}_endYear_Template.xlsx'
        newPath = os.path.join(basepath,'downloads',filename)

        
        bg = op.load_workbook(templatePath)
        sheet1 = bg['Sheet1']
        sheet2 = bg['Username and passwords']
        sheet1.cell(column = 4, row =1, value = sch_name.capitalize())
        sheet2.cell(column = 1, row =1, value = sch_name.capitalize())

        sql = "SELECT member_id, first_name, last_name, gender, member_age, ethnicity, \
            continuing_new, status, passport_number, passport_date_issued, \
            ethnicity_info, teaching_research, publication_promos, social_media,username,password FROM \
            members WHERE school_id = %s ORDER BY member_id" % schoolid 
        cur.execute(sql)
        mem_infos = cur.fetchall()
        for i in range(0,len(mem_infos)):
            mem_info = mem_infos[i][0:-2] 
            for j in range(1,len(mem_info)+1):
                sheet1.cell(column = j,row = 7+i,value = mem_info[j-1])
            u_p = list(mem_infos[i][1:3])+list(mem_infos[i][-2:])
            print(u_p,'uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu')
            for k in range(1,len(u_p)+1):
                sheet2.cell(column = k, row = 7+i, value = u_p[k-1])
            
        cur.execute("SELECT name, email, phone_number,username, password FROM coordinator \
            WHERE school_id  = %s;",(schoolid ,))
        coor = cur.fetchone()
        print(coor,'ccccccccccccccccccccccccccccccccccccccc')
        for i in range(1,len(coor[0:3])+1):
            sheet1.cell(column = 4,row = 1 + i,value = coor[0:3][i-1])
        coor_u_p = [coor[0],'Coordinator']+list(coor[-2:])
        for j in range(1,len(u_p)+1):
            sheet2.cell(column = j, row = 3, value = coor_u_p[j-1])


        
        

        bg.save(newPath)
        # return filename
        return newPath
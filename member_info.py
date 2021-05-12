import db
import pandas as pd




class members:
    def __init__(self,l=[]):
        self.id = l[0]
        self.first = l[1]
        self.last = l[2]
        self.gender = l[3]
        self.age = l[4]
        self.ethnicity = l[5]
        self.mtype = l[6]
        self.u_p = l[7]
        self.status = l[8]
        self.passport = l[9]
        self.last_year = l[10]
        self.date = l[11]
        self.eth_info = l[12]
        self.research = l[13]
        self.promos = l[14]
        self.social = l[15]
        self.term1 = l[16]
        self.term2 = l[17]
        self.term3 = l[18]
        self.term4 = l[19]
        self.total = l[20]
        self.username = l[21]
        self.password = l[22]
        self.school = l[23]
        self.gown = l[24]
        self.hat = l[25]

        self.event = l[26:-1] if len(l)>27 else False



    def insert_mem(self):
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
        cur.execute("INSERT INTO schools(school_id,school_name) VALUES (nextval('schoolid_seq'),%s) RETURNING school_id;",(school_name,))
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



def get_wb(excelpath):
    wb_school = pd.read_excel(excelpath,0,header=None,nrows=4)
    wb_school.dropna(axis='columns',how='all',inplace=True)
    wb_school.fillna('', inplace=True)
    name = wb_school.loc[0,3]
    print(wb_school)
    wb1 = pd.read_excel(excelpath,0,header=[5])
    wb1.iloc[:,10].fillna('NA', inplace=True)
    wb1.dropna(axis = 0, how='all', subset=['First Name','Last Name','Age'],inplace=True)
    wb1.fillna('', inplace=True)
    wb1.rename(columns={'#':'Memberid'},inplace = True)
    wb2 = pd.read_excel(excelpath,1,header=[5])
    wb1.insert(21,'USERNAME',wb2['USERNAME'].values)
    wb1.insert(22,'PASSWORD',wb2['PASSWORD'].values)
    wb1.insert(23,'School name',name)
    wb1.loc[:,'index'] = wb1.index
    wb_coor = pd.read_excel(excelpath,1,header=[1],nrows=1)
    wb_coor.dropna(axis='columns',how='all',inplace=True)
    wb_coor.loc[:,'School'] = wb_school.loc[0,3]
    wb_coor.loc[:,'Email'] = wb_school.loc[2,3]
    wb_coor.loc[:,'Phone'] = wb_school.loc[3,3]
    
    return [wb1,wb_coor]
def insert_coor(l=[]):
    cur = db.getCursor()
    school_id = get_schoolid(l[4])
    cur.execute("SELECT coordinator_id FROM coordinator where name = %s;",(l[0].lower(),))
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
    cur.execute("select * from coordinator;")
    print(cur.fetchall())



import db
import pandas as pd




class members:
    def __init__(self,l=[]):
        self.id = l[0]
        self.first = l[1]
        self.last = l[2]
        self.gender = l[3]
        self.age = l[3]
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
        self.gown = l[21]
        self.hat = l[22]
        self.username = l[23]
        self.password = l[24]
        self.school = l[25]
        self.event = l[26:] if len(l)>27 else False


    def insert_mem(self):
        cur = db.getCursor()
        
        sql = "UPDATE members SET school_id = %s, first_name = '%s', last_name = '%s', username='%s', password='%s', \
            gender='%s', member_age=%s, ethnicity='%s', continuing_new = '%s', passport_number='%s', passport_date_issued='%s', ethnicity_info='%s', \
            teaching_research='%s', publication_promos='%s', social_media='%s', gown_size='%s', hat_size='%s' WHERE member_id = %s;\
            " %(int(self.school), self.first, self.last, self.username, self.password, self.gender, int(self.age),self.ethnicity,
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
    return school_id
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
    wb_school = pd.read_excel(excelpath,0,header=None,nrows=3)
    wb_school.dropna(axis='columns',how='all',inplace=True)
    name = wb_school.loc[0,3]
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
    
    return wb1


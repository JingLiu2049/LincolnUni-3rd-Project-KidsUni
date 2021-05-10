import db

def get_id():
    cur = db.getCursor()
    cur.execute("INSERT INTO member VALUES (nextval('memberid'), null) RETURNING memberid;")
    memberid = cur.fetchone()[0]
    return memberid

class members:
    def __init__(self, id, first, last, gender, age, ethnicity, mtype, last_year, passport, date, eth_info, 
                research, promos, social, gown, hat, username, password, school):
        self.id = id
        self.first = first
        self.last = last
        self.gender = gender
        self.age = age
        self.ethnicity = ethnicity
        self.mtype = mtype
        self.last_year = last_year
        self.passport = passport
        self.date = date
        self.eth_info = eth_info
        self.research = research
        self.promos = promos
        self.social = social
        self.gown = gown
        self.hat = hat
        self.username = username
        self.password = password
        self.school = school
    def showid(self):
        return self.id

    
def mem_obj(l=[]):
    mem_obj = members(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],l[8],l[9],l[10],l[11],l[12],l[13],l[14],l[15],l[16],l[17],l[18])
    return mem_obj

# member1 = new_member([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17])
# print(member1.showid())

def fn(a,b,c,d,e):
    
    print('b = ',b, type(b))

fn(*(1,2,3,4,5))
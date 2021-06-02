import db

cur = db.getCursor()
class members:
    def __init__(self,l=[]):
        self.id = int(l[0])
        self.first = l[1]
        self.last = l[2]
        self.gender = l[3]
        self.age = l[4]
        self.ethnicity = l[5]
        self.mtype = l[6]

        self.status = l[7]
        self.passport = l[8] 
        
        self.date = l[9] if l[9] !='' else None
        self.eth_info = l[10]
        self.research = l[11]
        self.promos = l[12]
        self.social = l[13]

        self.username = l[14]
        self.password = l[15]
        self.school = l[16]

        self.previous = int(float(l[17]))
        self.term1 = int(float(l[18]))
        self.term2 = int(float(l[19]))
        self.term3 = int(float(l[20]))
        self.term4 = int(float(l[21]))
        self.total = int(float(l[22]))
        self.gown = l[23]
        self.hat = l[24]
        self.year = l[25]

        self.attend = l[26:-1] if len(l)>27 else False

    def hours(self, term_text, term_hour):
        # cur = db.getCursor()
        sql = f"INSERT INTO membershours VALUES({self.id}, '{self.year}', '{term_text}', \
            {term_hour}) ON CONFLICT (member_id, year, term) DO UPDATE SET member_id = EXCLUDED.member_id, \
            year = EXCLUDED.year, term = EXCLUDED.term, hours = EXCLUDED.hours;"
        cur.execute(sql)

    def insert_db(self,events=[]):
        # cur = db.getCursor()
        print(self.previous, 'sssssssssssssssssssssssssssssssssssssssssss')
        cur.execute("UPDATE members SET school_id = %s, first_name = %s, last_name = %s, username=%s, \
            password=%s, gender=%s, member_age=%s, ethnicity=%s, continuing_new = %s, \
             passport_number=%s, previous = %s, passport_date_issued=%s, ethnicity_info=%s, teaching_research=%s, \
             publication_promos=%s, social_media=%s, total = %s, gown_size=%s, hat_size=%s, status = %s WHERE \
             member_id = %s;",(self.school, self.first, self.last, self.username, self.password, self.gender, 
            self.age,self.ethnicity,self.mtype, self.passport, self.previous, self.date, self.eth_info, self.research, self.promos, 
            self.social, self.total, self.gown, self.hat, self.status,self.id,))
        if events:
            for i in range(0,len(events)):
                sql = "INSERT INTO attendance VALUES(%s, %s,'%s') ON CONFLICT (member_id, event_id) \
                DO UPDATE SET member_id = EXCLUDED.member_id, event_id = EXCLUDED.event_id,status = \
                EXCLUDED.status" %(self.id,events[i],self.attend[i])
                cur.execute(sql)

        self.hours('term1',self.term1)
        self.hours('term2',self.term2)
        self.hours('term3',self.term3)
        self.hours('term4',self.term4)

class volunteer:
    def __init__(self,l=[]):
        self.id = int(l[0])
        self.status = l[1]
        self.induction = l[2]
        self.interview = l[3]
        self.photo = l[4]
        self.studentid = int(l[5])
        self.firstname = l[6]
        self.surname = l[7]
        self.prefer = l[8]
        self.gender = l[9]
        self.birthday = l[10] if l[10] != '' else None
        self.email = l[11]
        self.phone = l[12]
        self.address = l[13]

        
        self.experience = l[14]
        self.leader = l[15]
        self.medical = l[16]
        self.police = l[17]
        self.emer_name = l[18]
        self.emer_relation = l[19]
        self.emer_phone = l[20]
        self.uni = l[21]
        self.graduate = l[22]
        self.course = l[23]
        self.current_year = l[24]
        self.comp_date = l[25]
        self.refer1_name = l[26]
        self.refer1_phone = l[27]
        self.refer1_emal = l[28]
        self.refer1_relation = l[29]
        self.refer2_name = l[30]
        self.refer2_phone = l[31]
        self.refer2_emal = l[32]
        self.refer2_relation = l[33]
        self.overview = l[34]
        self.session = l[35]
        self.role = l[36]
        self.consent = l[37]

        self.hours = l[38:-1] if len(l)>38 else False

    def insert_db(self,events):
        cur = db.getCursor()
        cur.execute("UPDATE volunteers SET  first_name = %s, surname = %s, preferred_name = %s, status = %s, student_id = %s, \
            gender = %s, dob = %s, email= %s,mobile= %s,address= %s, induction = %s, interview = %s, photo = %s \
            WHERE volun_id = %s",(self.firstname, self.surname, self.prefer,self.status,self.studentid,self.gender,self.birthday,
            self.email,self.phone,self.address, self.induction, self.interview, self.photo, self.id,))

        sql = f"INSERT INTO volunteerform VALUES({self.id},'{self.experience}',\
            '{self.leader}','{self.medical}','{self.police}','{self.emer_name}','{self.emer_relation}','{self.emer_phone}','{self.uni}',\
            '{self.graduate}','{self.course}','{self.current_year}','{self.comp_date}','{self.refer1_name}','{self.refer1_phone}',\
            '{self.refer1_emal}','{self.refer1_relation}','{self.refer2_name}','{self.refer2_phone}','{self.refer2_emal}',\
            '{self.refer2_relation}',$${self.overview}$$,$${self.session}$$,$${self.role}$$,$${self.consent}$$) ON CONFLICT (volun_id) DO UPDATE SET \
            volun_id = EXCLUDED.volun_id,  experience = \
            EXCLUDED.experience, future_leader = EXCLUDED.future_leader, medical_information= EXCLUDED.medical_information, police_check = \
            EXCLUDED.police_check, emer_name = EXCLUDED.emer_name, emerrelation = EXCLUDED.emerrelation, emer_phone = EXCLUDED.emer_phone, \
            studying_uni = EXCLUDED.studying_uni, graduated_uni = EXCLUDED.graduated_uni, course = EXCLUDED.course, current_year = EXCLUDED.current_year, \
            completion_date = EXCLUDED.completion_date, refer1_name = EXCLUDED.refer1_name, refer1_phone = EXCLUDED.refer1_phone, refer1_email = \
            EXCLUDED.refer1_email, refer1_relation = EXCLUDED.refer1_relation, refer2_name = EXCLUDED.refer2_name, refer2_phone = EXCLUDED.refer2_phone, \
            refer2_email = EXCLUDED.refer2_email, refer2_relation = EXCLUDED.refer2_relation, overview = EXCLUDED.overview, session = EXCLUDED.session, \
            role = EXCLUDED.role, consent = EXCLUDED.consent;"
        cur.execute(sql)
        if events:
            for i in range(0,len(events)):
                sql = "INSERT INTO volun_hours VALUES(%s, %s,%s) ON CONFLICT (volun_id, event_id) \
                DO UPDATE SET volun_id = EXCLUDED.volun_id, event_id = EXCLUDED.event_id, hours = \
                EXCLUDED.hours" %(self.id,int(events[i]),float(self.hours[i]))
                cur.execute(sql)

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
        self.agreement = l[13] if l[13] != '' else None
        self.rov = l[14] if l[14] != '' else None
        self.poster = l[15]
        self.logo = l[16]
        self.promo = l[17]
        self.photo = l[18]
        self.note = l[19]

        
        self.paperwork = l[20:] if len(l)>20 else False
    def insert_db(self,paperwork):
        cur = db.getCursor()
        cur.execute("UPDATE destinations SET status = %s, ld_name = %s, contact_person = %s, position = %s, \
            address = %s, region = %s, postal_address = %s, phone_number = %s,email = %s, web_address = %s, \
            member_cost = %s, adult_cost = %s, agrt_signed = %s, rov_signed = %s, poster_sent = %s, logo_sent = %s, \
            promo = %s, photo = %s, note = %s WHERE ld_id = %s;",(self.status, self.name, self.contact, self.position, self.address,
            self.region, self.post, self.phone, self.email, self.web, self.cost, self.adult_cost, self.agreement, self.rov,
            self.poster, self.logo, self.promo, self.photo, self.note, self.id, ))
        if paperwork:
            for i in range(0,len(paperwork)):
                sql = "INSERT INTO paperwork VALUES(%s, '%s','%s') ON CONFLICT (ld_id, year) \
                DO UPDATE SET ld_id = EXCLUDED.ld_id, year = EXCLUDED.year, status = \
                EXCLUDED.status" %(self.id,f'{paperwork[i]}-12-31',self.paperwork[i])
                cur.execute(sql)

    # def __del__(self):
    #     print('dest obj has been delated',self)

class criteria:
    def __init__(self, d = {}):
        self.key = [i for i in d.keys()][0]
        self.column = [i for i in d.values()][0][1]
        self.table = [i for i in d.values()][0][1]

import db
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
        self.gender = str(l[9]).lower()
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
        self.current_year = str(l[24]).lower()
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
            '{self.graduate}',$${self.course}$$,'{self.current_year}','{self.comp_date}','{self.refer1_name}','{self.refer1_phone}',\
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
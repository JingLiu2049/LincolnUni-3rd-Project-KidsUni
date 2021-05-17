import db
import pandas as pd
import openpyxl as op
import os
import datetime
import getid
from openpyxl import load_workbook

def gen_mem_temp(schoolid,filetype):
        # get template object
        basepath  = os.path.dirname(__file__)
        templatePath =os.path.join(basepath,'downloads','End year template.xlsx')
        bg = op.load_workbook(templatePath)
        sheet1 = bg['Sheet1']
        sheet2 = bg['Username and passwords']

        # generating new path 
        cur = db.getCursor()
        cur.execute("SELECT school_name FROM schools WHERE school_id = %s;",(schoolid ,))
        sch_name = cur.fetchone()[0]
        filename = f'{datetime.datetime.now().year}_{sch_name}_{filetype}.xlsx'
        newPath = os.path.join(basepath,'downloads',filename)
        
        # get member information from databse and insert into spreadsheet
        sheet1.cell(column = 4, row =1, value = sch_name.capitalize())
        sheet2.cell(column = 1, row =1, value = sch_name.capitalize())
        sql = "SELECT member_id, first_name, last_name, gender, member_age, ethnicity, \
            continuing_new, status, passport_number, passport_date_issued, \
            ethnicity_info, teaching_research, publication_promos, social_media,username,password FROM \
            members WHERE school_id = %s ORDER BY member_id" % schoolid 
        cur.execute(sql)
        mem_infos = cur.fetchall()
        if mem_infos:
            for i in range(0,len(mem_infos)):
                mem_info = mem_infos[i][0:-2] 
                for j in range(0,len(mem_info)):
                    sheet1.cell(column = j+1,row = 7+i,value = mem_info[j])
                u_p = list(mem_infos[i][1:3])+list(mem_infos[i][-2:])
                for k in range(0,len(u_p)):
                    sheet2.cell(column = k+1, row = 7+i, value = u_p[k])

        # get coordinator information from databse and insert into spreadsheet  
        cur.execute("SELECT name, email, phone_number,username, password FROM coordinator \
            WHERE school_id  = %s;",(schoolid ,))
        coor = cur.fetchone()
        for i in range(0,len(coor[0:3])):
            sheet1.cell(column = 4,row = 2 + i,value = coor[0:3][i])
        coor_u_p = [coor[0],'Coordinator']+list(coor[-2:])
        for j in range(0,len(u_p)):
            sheet2.cell(column = j+1, row = 3, value = coor_u_p[j])

        # get events info from databse and insert into spreadsheet
        # for template downloading, only insert event title
        if filetype =='template':
            cur.execute("SELECT name, event_id FROM events WHERE EXTRACT(YEAR FROM event_date) = \
                EXTRACT(year from now());")
            events = cur.fetchall()
            if events:
                for i in range(0,len(events)):
                    for j in range(0,2):
                        sheet1.cell(column = 23+i, row = 5+j, value = events[i][j])
            pd_sql = "SELECT * FROM events WHERE EXTRACT(YEAR FROM event_date) = EXTRACT(year from now()) \
                ORDER BY event_id;"
        # for completed downloading
        # insert event title
        if filetype =='completed':
            cur.execute("SELECT name, event_id FROM events ORDER BY event_id;")
            events = cur.fetchall()
            if events:
                for i in range(0,len(events)):
                    for j in range(0,2):
                        sheet1.cell(column = 23+i, row = 5+j, value = events[i][j])
        # get attendance info of each member and insert into spreadsheet
            for i in range(0,len(events)):
                eventid = events[i][1]
                sql = "SELECT attendance.status FROM members LEFT JOIN \
                attendance ON members.member_id = attendance.member_id WHERE members.school_id \
                = %s AND attendance.event_id = %s ORDER BY members.member_id" %(schoolid, eventid)
                cur.execute(sql)
                attends = cur.fetchall()
                for j in range(0,len(attends)):
                    sheet1.cell(column = 23+i, row = 7+j, value = attends[j][0])
            pd_sql = "SELECT * FROM events ORDER BY event_id;"

        #  save new excel file
        bg.save(newPath)

        #  insert new sheet for event details
        df = pd.read_sql(pd_sql,db.conn)
        book =load_workbook(newPath)
        writer = pd.ExcelWriter(newPath,engine='openpyxl')
        writer.book = book
        df.to_excel(writer,index=False,sheet_name='Events')
        writer.save()
        # return filename
        return newPath


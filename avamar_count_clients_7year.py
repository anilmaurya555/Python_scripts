#!/usr/bin/python
import pdb
import psycopg2
from smtplib import SMTP
import datetime
import argparse
retention = "%7Yr%"
date1 = "2021-09-29"
date2 = "2021-10-29"
servers = ('jcbamr300p','ppbamr302p','mnbamr302p','mnbamr303p')
for server in servers:
    print(server)
    conn = psycopg2.connect(host= server, port="5555", database="mcdb", user="viewuser", password="viewuser1")
    print ("Connected to Database")
    cur = conn.cursor()
    query = "SELECT COUNT(DISTINCT(client_name)) as Total FROM v_activities_2 "\
    "WHERE (recorded_date between '"+str(date1)+"' and '"+str(date2)+"' ) "\
    "and (v_activities_2.retention_policy like '"+str(retention)+"') ;"
    cur.execute(query)
    rows = cur.fetchall() 
    for row in rows:
            print(row)
    cur.close()
cur.close()
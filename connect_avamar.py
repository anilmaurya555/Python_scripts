# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:01:20 2021

@author: AMAURYA
"""

#!/usr/bin/env python
"""Groot Object Protection Report for python"""
from fnmatch import fnmatch
import psycopg2
from datetime import datetime
import codecs
# connect to groot
conn = psycopg2.connect(host="mnbamr303p.corpads.local", port="5555", database="mcdb", user="viewuser", password="viewuser1")
cur = conn.cursor()
sql_query = """
select host,CAST((elapsed/3600) as DECIMAL (10,2)) as Elasped_Time_Hour,status,CAST((bytes_scanned/1024/1024/1024) AS DECIMAL(10,3))as GB_SCANNED,CAST((bytes_new/1024/1024/1024) AS DECIMAL(10,3)) AS bytes_new_GB,pcntcommon from v_clientperftrack where started_ts between '2021-08-24' and '2021-08-25' and elapsed >=14400  ;
"""
cur.execute(sql_query)
rows = cur.fetchall()
print('{:<25} {:<15} {:<35} {:<15} {:<15} {:<10}'.format('host','Elapsed_time','status','GB_scanned','GB_new_bytes','dedup'))
print('=================================================================================================================')
csv='host,Elapsed_time,status,GB_scanned,GB_new_bytes,dedup\n'
for row in rows:
    (host,Elapsed_time,status,GB_scanned,GB_new_bytes,dedup)=row
    #print('%s  (%s)  %s  (%s)  %s  (%s)' % (host,Elapsed_time,status,GB_scanned,GB_new_bytes,dedup))
    print('{:<25} {:<15} {:<35} {:<15} {:<15} {:<10}'.format(host,Elapsed_time,status,GB_scanned,GB_new_bytes,dedup))
    csv +='%s,%s,%s,%s,%s,%s\n' %(host,Elapsed_time,status,GB_scanned,GB_new_bytes,dedup)
cur.close()
print ('Saving to CSV')
F=codecs.open('avamar.csv', 'w','utf-8')
F.write(csv)
F.close()
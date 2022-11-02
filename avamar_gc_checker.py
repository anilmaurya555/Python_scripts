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
servers = ('jcbamr300p','ppbamr302p','mnbamr302p','mnbamr303p')
print('{:<5} {:<15} {:<15} {:<15} {:<5} {:<10} {:<18} {:<15} {:<15} {:<10} {:<10}'.format('gcid','start_time','end_time','elapsed_time','result','node_count','indexstripes_total','indexstripes_processed','chunks_deleted','bytes_recovered','passes'))
csv='Avamar,gcid,start_time,end_time,elapsed_time,result,node_count,indexstripes_total,indexstripes_processed,chunks_deleted,bytes_recovered,passes\n'
for server in servers:
    # connect to groot
    print(server)
    conn = psycopg2.connect(host= server, port="5555", database="mcdb", user="viewuser", password="viewuser1")
    cur = conn.cursor()
    sql_query = """
    select gcstatusid,date(start_time) as start_date,date(end_time) as end_date,elapsed_time,result,node_count,indexstripes_total,indexstripes_processed,chunks_deleted,bytes_recovered,passes from v_gcstatus where start_time between '2021-11-10' and '2021-12-07';
    """
    cur.execute(sql_query)
    rows = cur.fetchall()
    for row in rows:
        (gcstatusid,start_time,end_time,elapsed_time,result,node_count,indexstripes_total,indexstripes_processed,chunks_deleted,bytes_recovered,passes)=row
        print('{:<5} {}   {}          {:<15} {:<5} {:<10} {:<18}      {:<15}             {:<15} {:<10} {:<10}'.format(gcstatusid,start_time,end_time,elapsed_time,result,node_count,indexstripes_total,indexstripes_processed,chunks_deleted,bytes_recovered,passes))
        csv +='%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %(server,gcstatusid,start_time,end_time,elapsed_time,result,node_count,indexstripes_total,indexstripes_processed,chunks_deleted,bytes_recovered,passes)
cur.close()
print ('Saving to CSV')
F=codecs.open('avamar_gc.csv', 'w','utf-8')
F.write(csv)
F.close()
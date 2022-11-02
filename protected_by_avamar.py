# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:01:20 2021
@author: AMAURYA
"""
#!/usr/bin/env python
"""Groot Object Protection Report for python"""
# command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--client', type=str, required=True)


args = parser.parse_args()
client = args.client
clientn = "'"+client+"%'"

from fnmatch import fnmatch
import psycopg2
from datetime import datetime
import codecs
#servers = ('jcbamr300p','ppbamr302p','mnbamr302p','mnbamr303p')
#servers = ('jcbamr300p')

# connect to groot
print(clientn)
conn = psycopg2.connect(host='jcbamr300p', port="5555", database="mcdb", user="viewuser", password="viewuser1")
cur = conn.cursor()
sql_query = """
select display_name,group_name,started_date,CAST((bytes_scanned/1024/1024/1024) AS DECIMAL(10,3)) as GB,plugin_name,schedule,status_code_summary from v_activities_2 where client_name like 'HWP00718%' and recorded_date_time > CURRENT_TIMESTAMP - interval '10 day';""" 
cur.execute(sql_query)
cur.fetchall()
cur.close()

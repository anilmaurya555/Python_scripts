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
select table_name from information_schema.tables;
"""
cur.execute(sql_query)
rows = cur.fetchall()
for row in rows:
    print (row)

cur.close()
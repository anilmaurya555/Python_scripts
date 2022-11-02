# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:01:20 2021

@author: AMAURYA
"""

#!/usr/bin/env python
"""Groot Object Protection Report for python"""
from pyhesity import *
from fnmatch import fnmatch
import psycopg2
from datetime import datetime
import codecs


# command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--vip', type=str, required=True)
parser.add_argument('-u', '--username', type=str, required=True)
parser.add_argument('-d', '--domain', type=str, default='local')

args = parser.parse_args()

vip = args.vip
username = args.username
domain = args.domain

# authenticate
apiauth(vip, username, domain)

print('Collecting report data...')

# get groot connection info from cluster
reporting = api('get', 'postgres', quiet=True)

cluster = api('get', 'cluster')
# connect to groot
conn = psycopg2.connect(host=reporting[0]['nodeIp'], port=reporting[0]['port'], database="postgres", user=reporting[0]['defaultUsername'], password=reporting[0]['defaultPassword'])
cur = conn.cursor()
sql_query = """
Select * from 
information_schema.columns where table_name = 'protection_job_run_archivals'; 
"""
cur.execute(sql_query)
cur.fetchall()

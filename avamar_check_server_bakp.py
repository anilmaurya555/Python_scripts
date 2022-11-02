#!/usr/bin/python
import pdb
import psycopg2
from smtplib import SMTP
import datetime
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--client', nargs='+', type=str, default=None)
parser.add_argument('-d1', '--date1', type=str, default=None)
parser.add_argument('-d2', '--date2', type=str, default=None)
parser.add_argument('-l', '--latest', action='store_true')

args = parser.parse_args()
client = args.client
date1 = args.date1
date2 = args.date2
latest = args.latest
allclients = [j.lower() +"%" for j in client]
#print (allclients)

servers = ('jcbamr300p','ppbamr302p','mnbamr302p','mnbamr303p')
for server in servers:
    print ("Connected to", server) 
    conn = psycopg2.connect(host= server, port="5555", database="mcdb", user="viewuser", password="viewuser1")
    print ("Connected to Database")
    cur = conn.cursor()
        
    if latest:
        for clientn in allclients:
            #print (clientn)
            query1 = "SELECT client_name,group_name,completed_date,ddr_hostname,domain,expiration,plugin_name,retention_policy,schedule,status_code,status_code_summary,type FROM v_activities_2 "\
                "WHERE (recorded_date_time > current_timestamp - interval '24 hours') "\
                    "and (v_activities_2.client_name like '"+str(clientn)+"');"
            cur.execute(query1)
            rows = cur.fetchall() 
            if len(rows) > 0:
                print('{:<25}|{:<15}|{:<15}|{:<15}|{:<5}|{:<10}|{:<18}|{:<15}|{:<15}|{:<10}|{:<10}'.format('client_name','group_name','completed_date','ddr_hostname','domain','expiration','plugin_name','retention_policy','schedule','status_code','status_code_summary','type'))
                print('================================================================================================================================================================')
                for row in rows:
                    (client_name,group_name,completed_date,ddr_hostname,domain,expiration,plugin_name,retention_policy,schedule,status_code,status_code_summary,type)=row
                    print('{:<25}|{:<15}|{}|{:<15}|{:<5}|{:<10}|{:<18}|{:<15}|{:<15}|{:<10}|{:<10}'.format(client_name,group_name,completed_date,ddr_hostname,domain,expiration,plugin_name,retention_policy,schedule,status_code,status_code_summary,type))
                    #cur.close()
    else:
        for clientn in allclients:
            query2 = "SELECT client_name,group_name,completed_date,ddr_hostname,domain,expiration,plugin_name,retention_policy,schedule,status_code,status_code_summary,type FROM v_activities_2 "\
                "WHERE (recorded_date between '"+str(date1)+"' and '"+str(date2)+"' ) "\
                    "and (v_activities_2.client_name like '"+str(clientn)+"') ;"
            cur.execute(query2)
            rows = cur.fetchall() 
            if len(rows) > 0:
                print('{:<25}|{:<15}|{:<15}|{:<15}|{:<5}|{:<10}|{:<18}|{:<15}|{:<15}|{:<10}|{:<10}'.format('client_name','group_name','completed_date','ddr_hostname','domain','expiration','plugin_name','retention_policy','schedule','status_code','status_code_summary','type'))
                print('================================================================================================================================================================')
                for row in rows:
                    (client_name,group_name,completed_date,ddr_hostname,domain,expiration,plugin_name,retention_policy,schedule,status_code,status_code_summary,type)=row
                    print('{:<25}|{:<15}|{}|{:<15}|{:<5}|{:<10}|{:<18}|{:<15}|{:<15}|{:<10}|{:<10}'.format(client_name,group_name,completed_date,ddr_hostname,domain,expiration,plugin_name,retention_policy,schedule,status_code,status_code_summary,type))
                    #cur.close()
    cur.close()
    
cur.close()
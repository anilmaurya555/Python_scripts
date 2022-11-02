#!/usr/bin/python
import pdb
import psycopg2
from smtplib import SMTP
import datetime
import argparse
import codecs
parser = argparse.ArgumentParser()
parser.add_argument('-d1', '--date1', type=str, default=None)
parser.add_argument('-d2', '--date2', type=str, default=None)
args = parser.parse_args()
date1 = args.date1
date2 = args.date2
outfile = 'Avamar_monthly_report-%s-%s.csv' % (date1, date2)
csv='Avamar_server,client_name,Backup scan in GB,group_name,display_full_domain,client_type,agent_version,os_type,retention_name,daily,weekly,monthly,yearly,schedule_name,ddr_hostname\n'
servers = ('jcbamr300p','ppbamr302p','mnbamr302p','mnbamr303p')
for server in servers:
    conn = psycopg2.connect(host= server, port="5555", database="mcdb", user="viewuser", password="viewuser1")
    print(server)
    print ("Connected to Database")
    cur = conn.cursor()
    query1 = "select clnt2.display_client_name,MAX(CAST((act.bytes_scanned/1024/1024/1024) AS DECIMAL(10,3))) as GB,mem.group_name,clnt2.display_full_domain,clnt2.client_type,clnt2.agent_version,clnt2.os_type,mem.retention_name,ret.daily,ret.weekly,ret.monthly,ret.yearly,grp.schedule_name,act.ddr_hostname from v_group_members mem,v_groups grp,v_clients clnt,v_clients_2 clnt2,v_activities_2 act,v_retention_policies ret where mem.group_name in (select name from v_groups where enabled='t') and mem.group_name=grp.name and mem.client_name=clnt.client_name and clnt.client_name=clnt2.client_name and clnt2.client_name=act.client_name and ret.name=mem.retention_name and act.started_date between '"+str(date1)+"' and '"+str(date2)+"' GROUP BY clnt2.display_client_name,mem.group_name,clnt2.display_full_domain,clnt2.client_type,clnt2.agent_version,clnt2.os_type,mem.retention_name,ret.daily,ret.weekly,ret.monthly,ret.yearly,grp.schedule_name,act.ddr_hostname "
    cur.execute(query1)
    rows = cur.fetchall() 
    for row in rows:
            (client_name,GB,group_name,display_full_domain,client_type,agent_version,os_type,retention_name,daily,weekly,monthly,yearly,schedule_name,ddr_hostname)=row
            csv +='%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' %(server,client_name,GB,group_name,display_full_domain,client_type,agent_version,os_type,retention_name,daily,weekly,monthly,yearly,schedule_name,ddr_hostname)
    cur.close()
cur.close()
print ('Saving to CSV')
F=codecs.open(outfile, 'w','utf-8')
F.write(csv)
F.close()
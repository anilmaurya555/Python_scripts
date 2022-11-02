#!/usr/bin/env python
"""Groot Object Protection Report for python"""
from pyhesity import *
from fnmatch import fnmatch
import psycopg2
from datetime import datetime
import codecs
#import smtplib
#from email.mime.multipart import MIMEMultipart
#from email.MIMEBase import MIMEBase
#from email import Encoders

# command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--vip', type=str, required=True)
parser.add_argument('-u', '--username', type=str, required=True)
parser.add_argument('-d', '--domain', type=str, default='local')
parser.add_argument('-n', '--numdays', type=int, default=31)
parser.add_argument('-f', '--filter', type=str, default=None)

args = parser.parse_args()

vip = args.vip
username = args.username
domain = args.domain
numdays = args.numdays
namefilter = args.filter


# authenticate
apiauth(vip, username, domain)

print('Collecting report data...')

# get groot connection info from cluster
reporting = api('get', 'postgres', quiet=True)
if 'errorCode' in reporting:
    print('statistics DB not found on %s' % vip)
    exit()

cluster = api('get', 'cluster')
# limit query to numdays
startUsecs = timeAgo(numdays, 'days')

# connect to groot
conn = psycopg2.connect(host=reporting[0]['nodeIp'], port=reporting[0]['port'], database="postgres", user=reporting[0]['defaultUsername'], password=reporting[0]['defaultPassword'])
cur = conn.cursor()

# sql query ----------------------------------------
sql_query = """
select
  pj.job_name as "Job Name",
  le.entity_name AS "Object Name",
  TRIM (
    leading 'k'
    from
      et.env_name
  ) as "Source Type",
  rs.source_name as "Source Name",
  jrs.status_name as "Job Status",
  'Backup' as task_type,
  ppolicy.name as "Policy Name",
  CASE
    WHEN jre.is_full_backup is True then 'Full'
    ELSE 'Incremental'
  END as "Full/Incremental",
  jre.source_delta_size_bytes as "Data Read",
  TO_CHAR(
    (TRUNC(jre.duration_usecs / 6e+7, 2) || ' minute') :: interval,
    'HH24:MI:SS'
  ) AS "Duration",
  to_char(to_timestamp(jre.start_time_usecs / 1000000), 'YYYY-MM-DD HH12:mmAM') as "Start Time",
  to_char(to_timestamp(jre.end_time_usecs / 1000000), 'YYYY-MM-DD HH12:mmAM') as "End Time",
  to_char(to_timestamp(pjr.snapshot_expiry_time_usecs / 1000000), 'YYYY-MM-DD HH12:mmAM') as "Expiry Date",
  CASE
    WHEN pjr.sla_violated is True then 'Yes'
    ELSE 'No'
  END as "SLA Violation",
  pjr.error_msg as "Failure Message"
from
  reporting.protection_job_run_entities jre,
  reporting.protection_jobs pj,
  reporting.leaf_entities le,
  reporting.job_run_status jrs,
  reporting.environment_types et,
  reporting.protection_job_runs pjr,
  reporting.registered_sources rs,
  reporting.protection_policy ppolicy
where
  jre.is_latest_attempt = true
  and jre.job_id = pj.job_id
  and jre.entity_id = le.entity_id
  and jre.status = jrs.status_id
  and jre.entity_env_type = et.env_id
  and jrs.status_name = 'Failure'
  and jre.job_run_id = pjr.job_run_id
  and jre.parent_source_id = rs.source_id
  and pj.policy_id = ppolicy.id
  and jre.start_time_usecs > %s
order by
  to_timestamp(jre.start_time_usecs / 1000000) desc;""" % startUsecs

now = datetime.now()
date = now.strftime("%m/%d/%Y %H:%M:%S")

csv = 'Job Name,Object Name,Source Type,Source Name,Job Status,Policy Name,Full/Incremental,Data Read,Duration,Start Time,End Time,Expiry Date,SLA Violation,Failure Message\n'

# get failures
cur.execute(sql_query)
rows = cur.fetchall()
for row in rows:
    (jobName, objectName, sourceType, sourceName, jobStatus, taskType, policyName, fullincr, dataread, duration, startTime, endTime, expiryDate, slaviolated, errormsg) = row
    if namefilter is None or fnmatch(objectName.lower(), namefilter.lower()) or fnmatch(sourceName.lower(), namefilter.lower()) or fnmatch(jobName.lower(), namefilter.lower()):
        csv += '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (jobName, objectName, sourceType, sourceName, jobStatus, policyName, fullincr, "%s MB" % (dataread / (1024 * 1024)), duration, startTime, endTime, expiryDate, slaviolated,errormsg)

cur.close()

if namefilter is not None:
    namefilterencoded = namefilter.replace('*', '_').replace('?', '_')
    outfileName = 'soxReport-%s-%s.csv' % (cluster['name'], namefilterencoded)
    subject = 'Cohesity Sox Report (%s) %s' % (cluster['name'], namefilterencoded)
else:
    outfileName = 'soxReport-%s.csv' % cluster['name']
    subject = 'Cohesity Sox Report (%s)' % cluster['name']

print('saving report as %s' % outfileName)
f = codecs.open(outfileName, 'w', 'utf-8')
f.write(csv)
f.close()

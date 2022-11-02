#!/usr/bin/env python
"""Python script to monitor a protectionJob"""

from pyhesity import *
import urllib
import time

VIP = 'cohesity651'
USERNAME = 'admin'
DOMAIN = 'local'
JOBNAME = 'win_bkp'
SLEEPTIME = 15  # seconds

apiauth(VIP, USERNAME)

f = open('lastrun', 'r')
lastRun = f.read()
f.close()
if lastRun == '':
    lastRun = timeAgo(1, 'sec')

print("Waiting for Cohesity Protection Job To Run...")

while True:
    jobId = api('get', 'protectionJobs?names=' + urllib.parse.quote_plus(JOBNAME))[0]['id']
    runs = api('get', 'protectionRuns?jobId=' + str(jobId))
    if 'startTimeUsecs' in runs[0]['backupRun']['stats']:
        latestRun = runs[0]['backupRun']['stats']['startTimeUsecs']
    if int(latestRun) > int(lastRun):  # job started since we last checked
        runURL = 'protectionRuns?startedTimeUsecs=%s&jobId=%s' % (latestRun, jobId)
        print(JOBNAME + ' started at ' + usecsToDate(latestRun))
        stillRunning = True
        while (stillRunning):
            state = api('get', runURL)
            if 'endTimeUsecs' in state[0]['backupRun']['stats']:
                result = state[0]['backupRun']['status']
                print(JOBNAME + ' ended with ' + result + ' at ' + usecsToDate(state[0]['backupRun']['stats']['endTimeUsecs']))
                stillRunning = False
            time.sleep(SLEEPTIME)
        lastRun = latestRun
        f = open('lastrun', 'w')
        f.write(str(lastRun))
        f.close()
    time.sleep(SLEEPTIME)
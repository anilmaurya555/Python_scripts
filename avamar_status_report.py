#!/usr/bin/python
import pdb
import psycopg2
from smtplib import SMTP
import datetime
#pdb.set_trace()

def sendreport(message_text):
    smtp = SMTP()
    smtp.connect('smtp.server.local', 25)
    from_addr = "Avamar grid <xxxx@.local>"
    to_addr = "admin@local.net"
    subj = "Avamar SQL Backup Exceptions"
    date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( from_addr, to_addr, subj, date, message_text )
    smtp.sendmail(from_addr, to_addr, msg)
    smtp.quit()

try:
        conn = psycopg2.connect('host=ppbamr302p port=5555 dbname=mcdb user=viewuser password=viewuser1')
        print ("Connected to Database")

except:
        print ("No Connection")

#cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur = conn.cursor()
#pdb.set_trace()
try:
    cur.execute("select client_name,domain,recorded_date,plugin_name,status_code FROM v_activities WHERE recorded_date_time > current_timestamp - interval '24 hours' AND plugin_name='Windows SQL'")
    rows = cur.fetchall()
    message_text = '\nServer\t\t\t\tResult'
    message_text += '\n--------\t\t\t--------'

    for row in rows:
        if (row[4] == 30000):
            result='Completed with succes.'
        elif (row[4] == 30005):
            result='Completed with exceptions.'
        elif (row[4] == 30999):
            result='Backup in error!'
        print ("Server: " + row[0] + "  Result: " + result)
        message_text += "\n" + row[0] + "\t\t" + result
    print ("Report: \n" + message_text)

except:
        print ("Not Working")
#sendreport(message_text)
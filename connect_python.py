from pyhesity import *
import psycopg2
apiauth('hcohesity01','amaurya','corpads.local')
cluster = api('get', 'cluster')
reporting = api('get', 'postgres', quiet=True)
conn = psycopg2.connect(host=reporting[0]['nodeIp'], port=reporting[0]['port'], database="postgres", user=reporting[0]['defaultUsername'], password=reporting[0]['defaultPassword'])
cur = conn.cursor()
cur.execute("Select * from information_schema.columns where table_name = 'protection_job_run_archivals'")
rows = cur.fetchall()
for row in rows:
    print("%s\t%s" % (row[3], row[7]))
cur.close()

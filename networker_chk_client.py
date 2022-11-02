import requests as re
import json
re.packages.urllib3.disable_warnings()
url = "https://hld10252:9090/nwrestapi/v3/global/clients?fl=aliases,hostname"
auth = ('administrator', 'Changeme_12345')
r = re.get(url, auth=auth,verify=False)
nr =r.content
out=json.loads(nr)
#print(nr)
print(out['clients'])
print("=========================================")
print(out['clients'][0])
print("=========================================")
print(out['clients'][3])
print("=========================================")
print(out['clients'][3]['aliases'])
print("=========================================")
print(out['clients'][3]['hostname'])
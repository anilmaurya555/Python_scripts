#version 1.0
## usage .\clusterinfo.py -v clustername -u username
#import pyhesity wrapper module
### import pyhesity wrapper module
from pyhesity import *
import datetime

### command line arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--vip', type=str, required=True)
parser.add_argument('-u', '--username', type=str, required=True)
parser.add_argument('-i', '--useApiKey', action='store_true')
parser.add_argument('-l', '--listgflags', action='store_true')

args = parser.parse_args()
vip = args.vip
username = args.username
listgflags = args.listgflags
useApiKey = args.useApiKey

#authenticate
apiauth(vip,username)
cluster = api('get', 'cluster')

status = api('get', '/nexus/cluster/status')
config = status['clusterConfig']['proto']
chassisList = config['chassisVec']
nodeList = config['nodeVec']
nodeStatus = status['nodeStatus']
diskList = config['diskVec']

# cluster info
output('\n------------------------------------')
output('     Cluster Name: %s' % status['clusterConfig']['proto']['clusterPartitionVec'][0]['hostName'])
output('       Cluster ID: %s' % status['clusterId'])
output('   Healing Status: %s' % status['healingStatus'])
output('     Service Sync: %s' % status['isServiceStateSynced'])
output(' Stopped Services: %s' % status['bulletinState']['stoppedServices'])
output('------------------------------------')
for chassis in chassisList:
    # chassis info
    if 'name' in chassis:
        chassisname = chassis['name']
    else:
        chassisname = chassis['serial']
    output('\n   Chassis Name: %s' % chassisname)
    output('     Chassis ID: %s' % chassis['id'])
    output('       Hardware: %s' % chassis.get('hardwareModel', 'VirtualEdition'))
    gotSerial = False
    for node in nodeList:
        if node['chassisId'] == chassis['id']:
            # node info
            apiauth(node['ip'].split(':')[-1], username, quiet=True, useApiKey=useApiKey)
            nodeInfo = api('get', '/nexus/node/hardware_info')
            if gotSerial is False:
                output(' Chassis Serial: %s' % nodeInfo['cohesityChassisSerial'])
                gotSerial = True
            output('\n            Node ID: %s' % node['id'])
            output('            Node IP: %s' % node['ip'].split(':')[-1])
            output('            IPMI IP: %s' % node.get('ipmiIp', 'n/a'))
            output('            Slot No: %s' % node.get('slotNumber', 0))
            output('          Serial No: %s' % nodeInfo.get('cohesityNodeSerial', 'VirtualEdition'))
            output('      Product Model: %s' % nodeInfo['productModel'])
            output('         SW Version: %s' % node['softwareVersion'])
            for stat in nodeStatus:
                if stat['nodeId'] == node['id']:
                    output('             Uptime: %s' % stat['uptime'])

if listgflags:
    output('\n--------\n Gflags\n--------')
    flags = api('get', '/nexus/cluster/list_gflags')
    for service in flags['servicesGflags']:
        servicename = service['serviceName']
        if len(service['gflags']) > 0:
            output('\n%s:\n' % servicename)
        gflags = service['gflags']
        for gflag in gflags:
            flagname = gflag['name']
            flagvalue = gflag['value']
            reason = gflag['reason']
            output('    %s: %s (%s)' % (flagname, flagvalue, reason))

output('')
f.close()
print(output)
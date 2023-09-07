import napalm
import json
from pprint import pprint
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

network_devices=[]

nxos_config = {
  "hostname": '172.16.100.100',
  "username": 'admin',
  "password": 'cisco',
  "optional_args": {"port": 65000}
}

iosv1_config = {
  "hostname": '10.1.1.1',
  "username": 'cisco',
  "password": 'cisco',
}

iosv3_config = {
  "hostname": '10.3.3.3',
  "username": 'cisco',
  "password": 'cisco',
}

iosv4_config = {
  "hostname": '10.4.4.4',
  "username": 'cisco',
  "password": 'cisco',
}

nxos =  ['nxos',nxos_config]
iosv1 = ['ios',iosv1_config]
iosv3 = ['ios',iosv3_config]
iosv4 = ['ios',iosv4_config]

routers= [nxos,iosv1,iosv3,iosv4]

for router in routers:
    driver=napalm.get_network_driver(router[0])
    device=driver(**router[1])
    device.open()
    bgp=device.get_bgp_neighbors()
    facts=device.get_facts()
    bgp['hostname']= facts['hostname']
    network_devices.append(bgp)
    device.close()

for item in network_devices:
    print( '-' * 50)
    print(item['hostname'])
    print( '-' * 50)
    for j in item['global']['peers']:
        if item['global']['peers'][j]['is_up'] == True:
                print( 'neighbour ' + j + ' is Established')
        else:
                print( 'neighbour ' + j +'  down')

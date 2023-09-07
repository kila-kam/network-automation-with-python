import napalm
import json
driver=napalm.get_network_driver('ios')
device=driver(hostname='10.1.1.1',username='cisco', password='cisco')
device.open()
print(device.get_config(retrieve='running',full=False))
print(device.get_environment())
bgp=device.get_bgp_neighbors()
device.close()

  for item in bgp['global']['peers']:
  	if bgp['global']['peers'][item]['is_up'] == True:
  		print(item +'is '+ 'Established')
  	else:
  		print(item +'is '+ 'down')

import napalm
import json
from pprint import pprint

routers= ['10.1.1.1','10.3.3.3','10.4.4.4']
network_devices=[]

for router in routers:
        driver=napalm.get_network_driver('ios')
        device=driver(hostname=router,username='cisco', password='cisco')
        device.open()
        facts=device.get_facts()
        bgp=device.get_bgp_neighbors()
        pprint(facts)
        network_devices.append(facts)
        device.close()

for item in network_devices:
        print( ' name:{} model: {} vendor:{} S/N: {}' .format(item['hostname'],item['model'],item['vendor'],item['serial_number']))

# name:vIOS1 model: IOSv vendor:Cisco S/N: 9B2BC2NH3PLQP0XKF72FU
#name:vIOS3 model: IOSv vendor:Cisco S/N: 9JU4IOYKGTC1U3LTIWAF8
 #name:vIOS4 model: IOSv vendor:Cisco S/N: 9ZZKU9S2L8R0VSXO3BLO0

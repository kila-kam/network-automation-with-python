from netmiko import ConnectHandler 
from getpass import getpass
import yaml
from pprint import pprint
from datetime import datetime
import textfsm

yml_file = open('/home/kkamson/.netmiko.yml', 'r') 
netdevices = yaml.load(yml_file)
#pprint(netdevices) 

devices=[netdevices['nxos1'],netdevices['nxos2']]

for device in devices:
	print(device)
	net_connect = ConnectHandler(**device)
	output=net_connect.send_config_from_file(config_file='changes.txt')
	print(output)
	net_connect.save_config()
	net_connect.disconnect()

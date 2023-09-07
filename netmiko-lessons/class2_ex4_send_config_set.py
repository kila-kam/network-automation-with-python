
from netmiko import ConnectHandler 
from getpass import getpass 
import yaml
from pprint import pprint
from datetime import datetime
import textfsm

yml_file = open('/home/kkamson/.netmiko.yml', 'r') 
netdevices = yaml.load(yml_file)
#pprint(netdevices) 

device =netdevices['cisco3']

print(device)
net_connect = ConnectHandler(**device)
cfg = [
     'ip name-server 1.1.1.1',
     'ip name-server 1.0.0.1',
     'ip domain-lookup'
      ]
output=net_connect.send_config_set(cfg)
pprint(output)
net_connect.disconnect()

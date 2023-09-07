
from netmiko import ConnectHandler 
from getpass import getpass 
import yaml
from pprint import pprint
from datetime import datetime
import textfsm

yml_file = open('/home/kkamson/.netmiko.yml', 'r') 
netdevices = yaml.load(yml_file)
#pprint(netdevices) 

device =netdevices['cisco4']

print(device)
net_connect = ConnectHandler(**device)
output=net_connect.send_command("show version",use_textfsm=True)
output2= net_connect.send_command("show lldp neighbors",use_textfsm=True)
pprint(output)
pprint(output2)
net_connect.disconnect()

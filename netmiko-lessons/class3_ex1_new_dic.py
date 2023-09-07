from pprint import pprint
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
output= net_connect.send_command("show ip arp",use_textfsm=True)
net_connect.disconnect()
new_list = []
for i in output:
    new_dict={}
    new_dict['mac_addr']=i['mac']
    new_dict['ip_addr']=i['address']
    new_dict['interface']=i['interface']
    new_list.append(new_dict)

pprint(new_list)

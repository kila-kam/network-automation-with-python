from netmiko import ConnectHandler 
from getpass import getpass 
import yaml
from pprint import pprint
from datetime import datetime

yml_file = open('/home/kkamson/.netmiko.yml', 'r') 
netdevices = yaml.load(yml_file)
#pprint(netdevices) 

device =netdevices['nxos2']
device['global_delay_factor']= 3

print(device)
net_connect = ConnectHandler(**device)
print(str(datetime.now()))
output= net_connect.send_command('show lldp neighbors ')
print(output)
print(str(datetime.now()))
output= net_connect.send_command('show lldp neighbors',delay_factor=8)
print(output)
print(str(datetime.now()))
net_connect.disconnect()


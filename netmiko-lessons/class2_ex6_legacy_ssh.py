
from netmiko import ConnectHandler 
from getpass import getpass 
import yaml
from pprint import pprint
from datetime import datetime
import textfsm
import time

yml_file = open('/home/kkamson/.netmiko.yml', 'r') 
netdevices = yaml.load(yml_file)
#pprint(netdevices) 

device =netdevices['cisco4']
device['session_log']='my_output.txt'
print(device)
net_connect = ConnectHandler(**device)
print(net_connect.find_prompt())
net_connect.config_mode()
print(net_connect.find_prompt())
print(net_connect.exit_config_mode())
yo= net_connect.write_channel('disable\n')
time.sleep(5)
output=net_connect.read_channel()
print(output)
net_connect.disconnect()

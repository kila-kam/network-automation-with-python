from netmiko import ConnectHandler 
from getpass import getpass 
import yaml
from pprint import pprint

yml_file = open('/home/kkamson/.netmiko.yml', 'r') 
netdevices = yaml.load(yml_file)
#pprint(netdevices)

net_connect = ConnectHandler(**netdevices['cisco3'])
net_connect.send_command_timing('ping')
net_connect.send_command_timing(' ')
net_connect.send_command_timing('8.8.8.8')
net_connect.send_command_timing(' ')
net_connect.send_command_timing(' ')
net_connect.send_command_timing(' ')
net_connect.send_command_timing(' ')
output= net_connect.send_command_timing('\n')

net_connect.disconnect()
print (output)




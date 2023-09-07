from netmiko import ConnectHandler 
from getpass import getpass 
import yaml
from pprint import pprint


yml_file = open('/home/kkamson/.netmiko.yml', 'r') 
netdevices = yaml.load(yml_file)
#pprint(netdevices) 




net_connect = ConnectHandler(**netdevices['cisco3']) 
net_connect.send_command('ping', expect_string='Protocol')
net_connect.send_command(' ', expect_string='Target')
net_connect.send_command('8.8.8.8 ', expect_string='Repeat')
net_connect.send_command(' ', expect_string='Datagram')
net_connect.send_command(' ', expect_string='Timeout')
net_connect.send_command(' ', expect_string='Extended')
net_connect.send_command(' ', expect_string='Sweep')
output= net_connect.send_command('\n',expect_string=r'#',strip_prompt=False, strip_command=False)
net_connect.disconnect()
print (output)

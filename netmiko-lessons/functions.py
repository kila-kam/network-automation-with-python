from netmiko import ConnectHandler
from jnpr.junos import Device
from datetime import datetime
from lxml import etree
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor, wait
from devices import *
import os
import paramiko
from subprocess import Popen, PIPE, STDOUT



#" ===================================== IOS,ARISTA, ==============================================================================================="

#This Module checks for todays logs on cisco devices

def show_logging(device):
    try:
        todays_date = datetime.now().strftime('%b %d')
        #print(todays_date)
        device = ConnectHandler(**device)
        device.enable()
        print('\n\n')
        print(device.find_prompt())
        print('=============\n\n')
        output=device.send_command('show logging').splitlines()
        log = False
        for log_output in output:
            if todays_date in log_output:
                print(log_output)
                log = True
        if log == False:
            print('\nNo logs generated today\n\n')
        device.disconnect()
    except  Exception as e:
        print(e)


def show_int_desc(device):
    try:
        device = ConnectHandler(**device)
        device.enable()
        print('\n\n')
        print(device.find_prompt())
        print('=============\n\n')
        new_connection.send("sh int des | i enc\n")
        time.sleep(3)
        output = new_connection.recv(max_buffer)
        #print(output)
        if output.count("up") == 4 :
            print('\n\nVB interfaces.................................... UP\n')
        else :
            print ('\n\nVB interfaces.................................... DOWN\n')
        device.disconnect()
    except  Exception as e:
        print(e)

def show_intf_desc_vb(device):
    try:
        device = ConnectHandler(**device)
        device.enable()
        print('\n\n')
        print(device.find_prompt())
        print('=============\n\n')
        output=device.send_command('sh int des | i enc')
        if output.count("up") == 4 :
            print('\n\nVB interfaces.................................... UP\n')
        else :
            print('\n\nVB interfaces.................................... DOWN\n')
    except  Exception as e:
        print(e)

def bgp_vb(device):
    try:
        device = ConnectHandler(**device)
        device.enable()
        print('\n\n')
        print(device.find_prompt())
        print('=============\n\n')
        output = device.send_command('sh ip bg neighbors | in BGP neighbor is')
        output += device.send_command('sh inter Gi0/1 desc')
        if 'BGP neighbor is 1.2.3.4,  remote AS 100, external link' in output and output.count('up') ==2 :
            print ('\n\nVB Internet.................................... OK\n')
        else :
            print ('\n\nVB Internet.................................... NOT OK\n')
    except  Exception as e:
        print(e)



def bgp_eurex(device):
    try:
        device = ConnectHandler(**device)
        device.enable()
        print('\n\n')
        print(device.find_prompt())
        print('=============\n\n')
        output = device.send_command('show ip bgp neighbors | in BGP neighbor is')
        if output.count("remote AS") == 3 :
            print('BGP interfaces.................................... OK\n')
        else :
            print('BGP interfaces.................................... NOT OK\n')
        eigrp = device.send_command('show ip eigrp  neighbors')
        #print(output)
        if ( eigrp.count("1.2.3.4")  or eigrp.count("1.2.3.4") ) == 1:
                print('EIGRP interfaces.................................... OK\n')
        else :
                print('EIGRP interfaces.................................... NOT OK\n')
        device.disconnect()
    except  Exception as e:
        print(e)


def show_intf_desc_internet(device):
  try:
    device = ConnectHandler(**device)
    device.enable()
    print('\n\n')
    print(device.find_prompt())
    print('=============\n\n')
    output = device.send_command('sh inter description | in terne')
    if output.count("up") == 6 :
      print('Internet interfaces .................................... OK\n')
    else :
      print ('Internet interfaces .................................... NOT OK\n')
    device.disconnect()
  except  Exception as e:
        print(e)


#"==================================================ASA==============================================================="

def  sh_crypto_isakmp(device):
    try:
        device = ConnectHandler(**device)
        device.enable()
        output=device.send_command('show crypto isakmp sa')
        ACTIVE_VPN=output.count('MM_ACTIVE')
        return ACTIVE_VPN
    except  Exception as e:
        print(e)


#"=============================================JUNIPER =================================================================="

#CHASSIS CLUSTER AND ALARMS
def show_chasis_cluster(device):
    dev = Device(**device)
    try:
        dev.open()
        result =dev.rpc.get_chassis_cluster_status()
#       session_count=result.find('.//').text
        dev.close()
    except  Exception as e:
        print(e)


#SESSION COUNT
def show_security_flow_session(device,prefix):
    dev = Device(**device)
    try:
        dev.open()
        for i in prefix:
                result =dev.rpc.get_flow_session_information(destination_prefix=i,summary=True,normalize=True)
                session_count=result.find('.//displayed-session-count').text
                print(" \n\nfor {} the number of sessions is  {} \n\n".format(i,session_count))
    except  Exception as e:
        print(e)

#IPSEC VPN COUNT
def show_ike_sec_assoc(device):
  try:
    ACTIVE_VPN = 0
    dev = Device(**device)
    dev.open()
    result  = dev.rpc.get_ike_security_associations_information()
    for ike_state in result.findall('.//ike-sa-state'):
      if ike_state.text == 'UP':
        ACTIVE_VPN +=1
    dev.close()
    return ACTIVE_VPN
  except  Exception as e:
        print(e)


def vpn():
  """
  Use concurrent futures threading to simultaneously gather "show version" output from devices.
  Wait for all threads to complete. Record the amount of time required to do this.
  """
  start_time = datetime.now()
  max_threads = 5

  # Create the thread pool
  pool = ThreadPoolExecutor(max_threads)

  # Create list to append threads to
  futures = []
  for device in vpns:
    if device in cisco_vpns:
      futures.append(pool.submit(sh_crypto_isakmp, device))
    else:
      futures.append(pool.submit(show_ike_sec_assoc, device))

  # Wait for all threads to complete.
  wait(futures)
  #print(futures)

  total=0

  for future in futures:
  # print(future.result())
  # print("\n\n")
    total+=future.result()

  print('\n\nTotal number of Active IPSec VPNs: {} ' .format(total))

  end_time = datetime.now()
  print("\n\n Finished in {}" .format(end_time - start_time))
  print("\n\n")


def show_bgp_summary(device):
  try:
    dev = Device(**device)
    dev.open()
    print('\n\n')
    print(dev.facts['hostname'])
    print('=============\n\n')
    bgp = dev.rpc.get_bgp_summary_information()
    data = []
    headers = ['peer ip', 'peer state', 'description', 'elaspsed time', 'flap count', 'status']
    for i in bgp.findall('bgp-peer'):
      elapsed_time = int(i.find('elapsed-time').attrib['seconds'])
      flap_count = int(i.find('flap-count').text)
      peer = i.find('peer-address').text
      if elapsed_time < 259200 and peer != '1.1.1.1':
        peer_state = i.find('peer-state').text
        description = i.find('description')
        if description == None:
          description = "No Description"
        else:
          description = i.find('description').text
        bgp_sum = [peer, peer_state, description, i.find('elapsed-time').text, i.find('flap-count').text]
        if peer_state != 'Established':
          bgp_neighbour_etree = dev.rpc.get_bgp_neighbor_information(neighbor_address=peer)
          bgp_sum.append('DOWN and FLAPPED RECENTLY')
          data.extend([bgp_sum])
        else:
          bgp_neighbour_etree = dev.rpc.get_bgp_neighbor_information(neighbor_address=peer)
          bgp_sum.append('FLAPPED RECENTLY')
          data.extend([bgp_sum])
    dev.close()
    if len(data) != 0:
      print(tabulate((data), headers=headers, tablefmt="grid"))
    else:
      print('\n BGP is All good, No flaps in the last 72 hours !!!\n ')

  except Exception as e:
    print(e)



def show_interface_detail(device):
  try:
    dev = Device(**device)
    dev.open()
    print('\n\n')
    print(dev.facts['hostname'])
    print('=============\n\n')
    result  = dev.rpc.get_interface_information(interface_name='[gxa]e*',extensive=True)
    dev.close()
    #print etree.dump(result)

    headers= ['name','intf-flap']
    data =[]

    error_count = 1
    t = float(error_count)

    "loop through object for attributes"

    for i in result.findall('physical-interface'):
      yo = i.find('name').text
      intf = yo.strip()
#      description = i.find('description')

#      if description == None:
#        description = "No Description"
#      else:
#        description = i.find('description').text
#        description = description.split()[1]
#    print(description)
      if  float(i.find('interface-flapped').attrib['seconds']) < 259200:
        flap ='flapped recently'
      else:
        flap = 'good'
      intf_list = [intf,flap]

      "loop through nested object append headers in header list  and values in intf list"

      for j in i.find('output-error-list'):
        if float(j.text) >= t and  j.tag not in headers:
          headers.append(j.tag)
          x= j.text
          intf_list.extend([x.strip()])
          continue
        if float(j.text) >= t and  j.tag  in headers:
          y = j.text
          intf_list.extend([y.strip()])

      for j in i.find('input-error-list'):
        if float(j.text) >= t and  j.tag not in headers:
          headers.append(j.tag)
          x= j.text
          intf_list.extend([x.strip()])
          continue
        if float(j.text) >= t and  j.tag  in headers:
          y = j.text
          intf_list.extend([y.strip()])

      "add intf list to empty data list "

      data.extend([intf_list])

#    print(data)
    print(tabulate(data,headers=headers,tablefmt="grid" ))
  except Exception as e:
    print(e)

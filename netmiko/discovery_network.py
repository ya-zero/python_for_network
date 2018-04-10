# -*- coding: utf-8 -*-
# опросить устройства в 192.168.0.0/24
# опросить устройство и сохранить информацию о оборудовании
#"Device Type","Mac","IP Address","Vlan","Boot ver","firmware ver"
#"SNR-S2965-24T","f8:f0:82:75:07:7c","7.0.3.5(R0241.0124)","7.2.25","192.168.0.195"
# заполнить таблицу device.db  sqlite  --> mysql
# аля многозадачность
import ipaddress
import subprocess
import netmiko
from pprint import pprint
#


def check_device (host):
      result=subprocess.run(['ping',str(host),'-c','1','-W','1'],stdout=subprocess.DEVNULL).returncode
      # returncode == 0  ping good
      return result

def connection_to_dev(device,commands):
   try:
     with netmiko.ConnectHandler(**device) as ssh:
          result=ssh.send_command(commands)
     return {device['ip']:result}
   except:
     print ('netmiko_return_error',device[ip])


password = 'test'
subnet=ipaddress.ip_network('192.168.0.195/32')
default_param={'device_type':'cisco_ios','username':'admin','password':password}
commands=['sh switch','sh version']

for device in subnet:
    if check_device(device) ==0:
      default_param.update({'ip':str(device)})
      result=connection_to_dev(default_param,commands[1])
      print (result)
      parse_s=result[str(device)].strip().split('\n')
      print (parse_s)

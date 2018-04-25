# -*- coding: utf-8 -*-
import csv
import telnetlib
import socket
import re
import time
import ipaddress
import subprocess
import getpass
subnet=ipaddress.ip_network('192.168.0.195/32')#а можно и так 192.168.0.0/24
#в данном случае в связи с отсутвием переменных при парсинге, header нужко указывать 
#в  какой последовательности идет  вывод с коммутатора.
switch_all=[['Device Type','Mac','IP Address','Vlan','Boot ver','firmware ver'],]
sw_pass=getpass.getpass('Password:').encode('utf-8')
print (sw_pass)
for host in subnet:
   if subprocess.run(['ping',str(host),'-c','1'],stdout=subprocess.DEVNULL).returncode==0:
    good=False
    try:
        a=telnetlib.Telnet(str(host),23,5)
        a.close()
        good=True
    except ConnectionRefusedError:
          pass
    except socket.timeout:
          pass

    if good:
         tel=telnetlib.Telnet(str(host))
         time.sleep(5)
         vendor=tel.read_very_eager()
         tel.write(b'admin'+b'\n')
         tel.write(sw_pass+b'\n')
         if b'UserName' in vendor:
           continue
           tel.write(b'sh switch'+b'\n')
           time.sleep(1)
           parse_sw=tel.read_very_eager()
           parse_s=str(parse_sw.decode('ascii')).strip().split('\n')
           switch_funcional=['device type','mac','vlan name','firmware ver','boot','ip address']
           switch_str=[]
           for elem in parse_s:
               for sw_i in switch_funcional:
                  if sw_i in elem.lower():
                     #print(elem.strip().split(':'))
                     #switch_str.append(elem.strip().split(':'))
                     switch_str.append(elem.strip().split(':')[1])
 
           if switch_str:
#              print (switch_str)
              switch_all.append(switch_str)
           tel.close()
         else:
          tel.write(b'sh version'+b'\n')
          time.sleep(1)
          parse_sw=tel.read_very_eager()
          parse_s=str(parse_sw.decode('ascii')).strip().split('\n')
#          print(parse_s)
          switch_funcional=[('device','\s*(SNR-\S+).*'),('vlan mac','.*Vlan MAC (\S+)'),('software ver','.*SoftWare Version (\S+)'),('bootrom','.*BootRom Version (\S+)')]
          switch_str=[]
#          regexp=('.*Vlan MAC (\S+)|.*(SNR\S+)|.*SoftWare Version (\S+)|.*BootRom Version (\S+)')
          for elem in parse_s:
              for sw_i,re_i in switch_funcional:
                 if sw_i in elem.lower():
#                    print (sw_i,re_i)
                    match=re.search(re_i,elem)
                    if match:
                        switch_str.append(match.group(1))

          if switch_str:
             switch_str.append(str(host))
             switch_all.append(switch_str)
          tel.close()


with open('switch.csv','w') as f:
     writer = csv.writer(f,quoting=csv.QUOTE_NONNUMERIC)
     for row in switch_all:
         writer.writerow(row)

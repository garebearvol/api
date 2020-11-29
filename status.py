import sched, socket, datetime
from time import time, sleep
import json
import re

with open('/home/pi/api/status.json') as f:
  zonestatus = json.load(f)



HOST2='192.168.1.115'
PORT2=4999

def Check_status(Zone):
    s=socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST2, PORT2))
    s.sendall(f"*Z0{Zone}CONSR\r".encode())
    sleep(3)
    response=str(s.recv(60))
    s.close
    print(response)
    if (f"Z0{Zone}PWRON" in response):
        zonestatus[f'{Zone}']['pwr']=True
        volresponse=(re.search('VOL-(.*),', response))
        vol=int(volresponse.group(1))
        zonestatus[f'{Zone}']['vol']=((60-(vol))/60)
    else:
        zonestatus[f'{Zone}']['pwr']=False
        zonestatus[f'{Zone}']['vol']=0
    sleep(2)

for x in range(1, 7):
    Check_status(x)


with open('/home/pi/api/status.json', 'w') as f:
    json.dump(zonestatus, f)

print(zonestatus)


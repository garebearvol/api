import sched, socket, datetime, json, re, os
from time import time, sleep

cwd=os.getcwd()
with open('{}/status.json'.format(cwd)) as f:
  zonestatus = json.load(f)

#RS-232 global cache info
HOST2='192.168.1.115'
PORT2=4999

def Check_status(Zone):
    s=socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST2, PORT2))
    s.sendall("*Z0{}CONSR\r".format(Zone).encode())
    sleep(3)
    response=str(s.recv(60))
    s.close
    print(response)
    if ("Z0{}PWRON".format(Zone) in response):
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


with open('{}/status.json'.format(cwd), 'w') as f:
    json.dump(zonestatus, f)

print(zonestatus)
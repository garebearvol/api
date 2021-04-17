import sched, socket, datetime, json, re, os
from time import time, sleep

cwd=os.getcwd()
with open('{}/status.json'.format(cwd)) as f:
  zonestatus = json.load(f)

ser = serial.Serial(
   port='/dev/ttyUSB0',
   baudrate=9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=3,
   inter_byte_timeout=.1
)

def Check_status(Zone):
    ser.close()
    ser.open()
    ser.write("*Z0{}CONSR\r".format(Zone))
    sleep(3)
    response=ser.readline()
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
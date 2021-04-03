import serial


ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=3,
    inter_byte_timeout=.1
)
ser.isOpen()
ser.write("*Z02CONSR\r")
response =  ser.readline()
print(response) 
ser.close()

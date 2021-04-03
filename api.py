#updated 3/9/2021
from flask import Flask
from flask_restful import Resource, Api
from flask import jsonify, request
import socket, json, time, threading, serial

app = Flask(__name__)
api = Api(app)

ser = serial.Serial(
   port='/dev/ttyUSB0',
   baudrate=9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=3,
   inter_byte_timeout=.1
)
ser.close()
def power_change(data):  
    ser.open()
    for x in range (1, 7):
        zpwr=data.get('pwr{}'.format(x))
        if zpwr is True:
            ser.write("*Z0{}ON\r".format(x))
            response =  ser.readline()
            ser.write("*Z0{}VOL20\r".format(x))
            response =  ser.readline()
        if zpwr is False:
            ser.write("*Z0{}OFF\r".format(x))
            response =  ser.readline()
    ser.close()
            
class status(Resource):
    def status():
        if request.method=='POST':
            posted_data = request.get_json()
            return jsonify(zonestatus)


@app.route("/off", methods=["POST"])
def off():
    if request.method=='POST':
         s=socket.socket( socket.AF_INET, socket.SOCK_STREAM)
         s.connect((HOST2, PORT2))
         s.sendall("*ALLOFF\r".encode())
         s.close
         return "All Speakers Off"


@app.route("/control", methods=["POST"])
def power():
    data= request.get_json()
    threading.Thread(target=power_change, args=(data,)).start()
    return jsonify('Response asynchronosly')

            

api.add_resource(status, '/status/')

if __name__=='__main__':
      app.run(host='0.0.0.0', port=8000)

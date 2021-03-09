#updated 3/9/2021
from flask import Flask
from flask_restful import Resource, Api
from flask import jsonify, request
import socket
import json
import time

with open('/home/pi/api/status.json') as f:
  zonestatus = json.load(f)

HOST2='192.168.1.115'
PORT2=4999

app = Flask(__name__)
api = Api(app)

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
    r= request.get_json()
    response=[]
    for x in range (1, 7):
        response=[]
        zpwr=r.get(f'pwr{x}')
        if zpwr is True:
            s =socket.socket( socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST2, PORT2))
            s.sendall(f"*Z0{x}ON\r".encode())
            s.close
            s =socket.socket( socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST2, PORT2))
            s.sendall(f"*Z0{x}VOL20\r".encode())
            response=str(s.recv(24))
            print("Response from the Speakers():", response)
            s.close
            time.sleep(1)
        if zpwr is False:
            s=socket.socket( socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST2, PORT2))
            s.sendall(f"*Z0{x}OFF\r".encode())
            s.close
            time.sleep(1)
    return str(response)
            

api.add_resource(status, '/status/')

if __name__=='__main__':
      app.run(host='0.0.0.0')

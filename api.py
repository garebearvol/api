#updated 3/9/2021
from flask import Flask
from flask_restful import Resource, Api
from flask import jsonify, request
import socket, json, time, threading

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
    def power_change():
        for x in range (1, 7):
            response=[]
            zpwr=r.get('pwr{}'.format(x))
            if zpwr is True:
                s =socket.socket( socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST2, PORT2))
                s.sendall("*Z0{}ON\r".format(x).encode())
                s.close
                s =socket.socket( socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST2, PORT2))
                s.sendall("*Z0{}VOL20\r".format(x).encode())
                response=str(s.recv(24))
                print("Response from the Speakers():", response)
                s.close
                time.sleep(1)
            if zpwr is False:
                s=socket.socket( socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST2, PORT2))
                s.sendall("*Z0{}OFF\r".format(x).encode())
                s.close
                time.sleep(1)
    thread=threading.Thread(target=power_change)
    thread.start()
    return {"message": "Accepted"}, 202
            

api.add_resource(status, '/status/')

if __name__=='__main__':
      app.run(host='0.0.0.0', port=8000)

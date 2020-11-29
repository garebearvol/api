import socket

HOST2='192.168.1.115'
PORT2=4999

def speaker_on(speaker):
	for x in speaker:
		print(x)
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
speakers=[3, 4]	
speaker_on(speakers)

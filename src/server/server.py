import socket			
from threading import Thread, active_count
from dataclasses import dataclass
from time import sleep
from json import loads
from playsound import playsound


AUDIO = 'audio.mp3'

@dataclass
class Chatserver:
	PORT: int = 4000
	SERVER: str = socket.gethostbyname(socket.gethostname())
	SOCKET: socket = socket.socket()
	HEADER: int = 10
	FORMAT: str = "utf-8"
	DISCONNECTING: str = "!DISCONNEC"
	
	
	def connect(self, conn, address):
		print(f"NEW CONNECTION  {address}")
		t = Thread(target=playsound, args=(AUDIO, ))
		connected = True
		while connected:
			msg_len = conn.recv(self.HEADER).decode(self.FORMAT)
			msg_len = int(msg_len)
			msg = conn.recv(msg_len).decode(self.FORMAT)
			msg = loads(msg)
			print(msg)
			username, message = msg["name"], msg["msg"]
			if msg == self.DISCONNECTING:
				connected = False
			print(f"{username} said: {message}")
			sleep(40)

	def start(self):
		self.bind_()
		self.SOCKET.listen(10)
		print(f"Server Started {socket.gethostname()}@{self.SERVER}:{self.PORT}")
		while True:
			conn, address = self.SOCKET.accept()
			Thread_ = Thread(target=self.connect, args=(conn, address))
			Thread_.start()
			Thread_.join()
			print(f"Active users: {active_count() - 1}")

	def bind_(self):
		self.SOCKET.bind((self.SERVER, self.PORT))

	def close(self):
		self.SOCKET.close()

s = Chatserver()
s.start()
s.close()
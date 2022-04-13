import socket			
from threading import Thread, active_count
from dataclasses import dataclass, field
from time import sleep
from json import loads, dumps
# from colorama import Fore
# from playsound import playsound


# AUDIO = 'audio.mp3'

@dataclass
class Chatserver:
	clients: list = field(default_factory=list)
	PORT: int = 4000
	SERVER: str = socket.gethostbyname(socket.gethostname())
	SOCKET: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	HEADER: int = 10
	FORMAT: str = "utf-8"
	DISCONNECTING: str = "!DISCONNECT"
	
	def connect(self, conn, address):
		print(f"NEW CONNECTION {address}")
		self.clients.append(conn)
		connected = True
		while connected:
			msg_len = conn.recv(self.HEADER).decode(self.FORMAT)
			msg_len = int(msg_len)
			msg = conn.recv(msg_len).decode(self.FORMAT)
			msg = loads(msg)
			if msg["msg"] == self.DISCONNECTING:
				connected = False
			self.broadcast(msg)

	def broadcast(self, msg):
		for client in self.clients:
			msg = dumps(msg)
			client.send(str(len(msg)).encode(self.FORMAT))
			client.send(msg.encode(self.FORMAT))

	def start(self):
		self.bind_()
		self.SOCKET.listen(10)
		print(f"Server Started {socket.gethostname()}@{self.SERVER}:{self.PORT}")
		while True:
			conn, address = self.SOCKET.accept()
			Thread_ = Thread(target=self.connect, args=(conn, address))
			Thread_.start()
			print(f"Active users: {active_count() - 1}")

	def bind_(self):
		self.SOCKET.bind((self.SERVER, self.PORT))

	def close(self):
		self.SOCKET.close()

s = Chatserver()
s.start()
s.close()
import socket
from dataclasses import dataclass
from json import dumps


@dataclass
class Client:
	PORT: int = 4000
	SERVER: str = socket.gethostbyname(socket.gethostname())
	SOCKET: socket = socket.socket()
	HEADER: int = 64
	DISCONNECTING: str = "!DISCONNEC"
	FORMAT: str = "utf-8"
	USERNAME: str = None

	def setup(self):
		self.login()

	def login(self):
		self.USERNAME = input("Enter your name :")
		print(f"THANKS! {self.USERNAME}")

	def connect(self):
		self.SOCKET.connect((self.SERVER, self.PORT))
		self.setup()
		self.prepareMessage()

	def close(self):
		self.SOCKET.close()
	def prepareMessage(self):
		run = True
		while run:
			MSG = input(f"Send A Hello to {socket.gethostname()}@{self.SERVER}: ")
			
			MSG = {
				"msg": MSG,
				"name": self.USERNAME
			}

			self.send(dumps(MSG))
	def send(self, msg: str):
		msg = msg.encode(self.FORMAT)
		self.SOCKET.send(str(len(msg)).encode(self.FORMAT))
		self.SOCKET.send(msg)
		print("Sent")

	@property
	def properties(self):
		return [i for i in dir(self.SOCKET) if not str(i).startswith("__")]

client_ = Client()
client_.connect()
client_.close()

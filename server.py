from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread

class Server:
  def __init__(self, address: str, port: int) -> None:
    self.address: str = address
    self.port: int = port
    self.players: int = 0
    self.started: bool = False
    self.MAX_PLAYERS: int = 5
    self.__start()
    self.__listen()

  def __start(self) -> None:
    self.server: socket = socket(AF_INET, SOCK_DGRAM)
    self.server.bind((self.address, self.port))
    print(f'Server is running at {self.address}:{self.port}')

  def __listen(self):
    while True:
      data, client_adress = self.server.recvfrom(2048)
      self.__send_data(f"Hello {client_adress}! I've received this from you: {data.decode()}", client_adress)

  def __send_data(self, data: str, client_address):
    self.server.sendto(data.encode(), client_address) 


servidor_udp = Server('localhost', 8080)

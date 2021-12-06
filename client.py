from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread

class Client:
  def __init__(self, address: str, port: int):
    self.address: str = address
    self.port: int = port
    self.socket: socket = socket(AF_INET, SOCK_DGRAM)
    self.allowed: bool = False
    self.answered: bool = True
    Thread(target=self.__listen_server).start()
    self.__listen_keyboard()
  
  def __listen_keyboard(self):
    while True:
      if not self.answered: continue
      if not self.allowed:
        message = input('send ? to know if you can join the game: ')
        if message == '?':
          self.__send_message(message)
        else:
          print("ops.. it seems that you write some different. Let's try again")
          continue
      else:
        message = input('send ! to notify that you are ready: ')
        if message == '!':
          self.__send_message(message)
        else:
          print("ops.. it seems that you write some different. Let's try again")
          continue

  def __send_message(self, message: str):
    self.answered = False
    self.socket.sendto(message.encode(), (self.address, self.port))

  def __listen_server(self):
    while True:
      data = self.socket.recv(2048)
      self.answered = True
      print(data.decode())

cliente = Client('localhost', 8080)

from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread

class Client:
  def __init__(self, address: str, port: int):
    self.address: str = address
    self.port: int = port
    self.socket: socket = socket(AF_INET, SOCK_DGRAM)
    self.must_wait: bool = False
    self.answered: bool = True
    self.is_playing: bool = False
    Thread(target=self.__listen_server).start()
    self.__listen_keyboard()
  
  def __listen_keyboard(self):
    while True:
      if self.must_wait: continue
      message = input('send: ')
      self.must_wait = True
      self.__send_message(message)

  def __send_message(self, message: str):
    self.answered = False
    self.socket.sendto(message.encode(), (self.address, self.port))

  def __listen_server(self):
    while True:
      data = self.socket.recv(2048)
      data = data.decode()
      if data == '...':
        print('Waiting for match to start. You will be notified when it occurs...')
      elif data == '---':
        print('--- MATCH STARTED ---')
      elif data.startswith('R.'):
        print(data)
      else:
        self.must_wait = False
        print(data)

cliente = Client('localhost', 8080)

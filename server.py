from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread

class Server:
  def __init__(self, address: str, port: int) -> None:
    self.address: str = address
    self.port: int = port
    self.players = []
    self.ranking = {}
    self.answers = {}
    self.started: bool = False
    self.MAX_PLAYERS: int = 5
    Thread(target=self.__match_manager).start()
    self.__mount_questions()
    self.__start()
    self.__listen()

  def __mount_questions(self):
    questions = []
    with open('questions.txt', 'r') as file:
      for line in file.readlines():
        question, answer = line.split(',')
        questions.append({
          "title": question[1:],
          "answer": answer[0:-2],
        })

    self.questions = questions

  def __start(self) -> None:
    self.server: socket = socket(AF_INET, SOCK_DGRAM)
    self.server.bind((self.address, self.port))
    print(f'Server is running at {self.address}:{self.port}')

  def __is_registrated(self, address) -> bool:
    return address in self.players

  def __can_get_in(self) -> bool:
    return not self.started and len(self.players) < self.MAX_PLAYERS

  def __notify_init_game(self):
    for player in self.players:
      self.__send_data('---', player)

  def __manage_info(self, data: str, client_address) -> None:
    if (data == '?' and not self.__is_registrated(client_address) and self.__can_get_in()):
      self.players.append(client_address)
      print(f'Player indentified by {client_address} address joined the match!')
      self.__send_data("You joined the match. Send '!' to notify that you are ready",  client_address)

    elif (data == '?' and not self.__is_registrated(client_address) and not self.__can_get_in()):
      self.__send_data('Now you cannot join the game. Try again later...', client_address)

    elif (data == '?' and self.__is_registrated(client_address) and not self.started):
      self.__send_data('Waiting for all players to get ready...', client_address)

    elif (data == '!' and not self.__is_registrated(client_address)):
      self.__send_data('You are not in the match to be ready. SORRY :(', client_address)

    elif (data == '!' and self.__is_registrated(client_address) and not self.started):
      print(f'Player {client_address} is ready to play!')
      self.ranking[client_address] = 0
      if len(self.ranking.keys()) == 1:
        self.__send_data('...', client_address)
      elif len(self.ranking.keys()) == len(self.players):
        self.__notify_init_game()
        self.started = True
      else:
        self.__send_data('...', client_address)

  def __listen(self):
    while True:
      data, client_adress = self.server.recvfrom(2048)
      self.__manage_info(data.decode(), client_adress)

  def __match_manager(self) -> None:
    while True:
      if not self.started: continue
      print('started')
      self.started = False


  def __send_data(self, data: str, client_address):
    self.server.sendto(data.encode(), client_address) 


servidor_udp = Server('localhost', 8080)

from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from random import randint
from time import time

class Server:
  def __init__(self, address: str, port: int) -> None:
    self.address: str = address
    self.port: int = port
    self.__init_data()
    self.MAX_PLAYERS: int = 5
    Thread(target=self.__counter).start()
    self.__mount_questions()
    self.__start()
    self.__listen()

  def __init_data(self):
    self.players: list = []
    self.ranking: dict = {}
    self.answers: dict = {}
    self.started: bool = False
    self.round: int = 1
    self.drawns: list = []
    self.round_running: bool = False

  def __new_round(self):
    self.answers = {}
    self.round += 1

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
      self.__send_data('You are not in the match. SORRY :(', client_address)

    elif (data == '!' and self.__is_registrated(client_address) and not self.started):
      print(f'Player {client_address} is ready to play!')
      self.ranking[client_address] = 0
      if len(self.ranking.keys()) == 1:
        self.__send_data('...', client_address)
      elif len(self.ranking.keys()) == len(self.players):
        self.__notify_init_game()
        print('--- MATCH STARTED ---')
        self.started = True
        self.__manage_question()
      else:
        self.__send_data('...', client_address)

    elif not self.__is_registrated(client_address):
      self.__send_data('You are not in a match', client_address)

    elif not client_address in self.answers.keys():
      self.__send_data('...', client_address)
      self.__match_manager(data, client_address)

  def __listen(self):
    while True:
      data, client_adress = self.server.recvfrom(2048)
      self.__manage_info(data.decode(), client_adress)

  def __drawn_question(self) -> None:
    is_avlid = False
    while not is_avlid:
      index = randint(0, 19)
      if index not in self.drawns:
        self.drawns.append(index)
        is_avlid = True

  def __send_questions(self) -> None:
    for player in self.players:
      self.__send_data(self.questions[self.drawns[-1]]['title'], player)

  def __manage_question(self):
    self.round_running = False
    self.__drawn_question()
    self.__send_questions()
    self.round_running = True

  def __round_manager(self):
    self.round_running = False
    for player in self.players:
      answer = self.answers.get(player, None)
      if answer == None:
        self.ranking[player] -= 1
        self.__send_data('R. You have not responded', player)
      elif answer == self.questions[self.drawns[-1]]['answer']:
        self.ranking[player] += 25
      else:
        self.ranking[player] -= 5

    if self.round == 5:
      for player in self.players:
        self.__send_data('#', player)
      self.__init_data()
    else:
      self.__new_round()
      self.__manage_question()

  def __match_manager(self, data, address) -> None:
    if not self.round_running: return
    if data == self.questions[self.drawns[-1]]['answer']:
      self.answers[address] = data
      self.__send_data('R. CORRECT :)', address)
      self.__round_manager()
    else:
      self.answers[address] = data
      self.__send_data('R. WRONG :(', address)
      if len(self.answers.keys()) == len(self.players):
        self.__round_manager()

  def __counter(self):
    while True:
      if not self.round_running: continue
      start = time()
      wait = True
      while wait:
        if not self.round_running: break
        if time() - start >= 10:
          wait = False

      if self.round_running: self.__round_manager()

  def __send_data(self, data: str, client_address):
    self.server.sendto(data.encode(), client_address) 


servidor_udp = Server('localhost', 8080)

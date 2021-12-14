# Socket TPC para transferência de arquivos HTML.

from os import path, chdir, mkdir
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from BrowsingFolder import BrowsingFolder


class ProtocolHTTP:
    def __init__(self, sender):
        self.sender = sender

    def handle_http(self, data: str):
        try:
            http_params = data.split('\r\n')
            http_header = http_params[0].split(' ')

            http_method = http_header[0]
            requested_file = http_header[1]
            http_version = http_header[2]

            print(
                f'Method: {http_method}; file: {requested_file}; version: {http_version}')

            self.handle_version(http_version)

            content = self.handle_method(
                http_method, f'/files{requested_file}')
            msg = self.get_message('200')
            self.handle_response(msg, content)

        except Exception as e:
            msg = self.get_message(repr(e))
            self.handle_response(msg, '<h1>NOT FOUND</h1>')

    @staticmethod
    def handle_method(method: str, all_path: str):
        if 'GET' in method:
            content = ''
            if path.isfile(all_path):
                with open(all_path, 'r') as file:
                    for line in file.readlines():
                        content += line
            elif path.isfile(f'{all_path}index.html'):
                with open(f'{all_path}index.html', 'r') as file:
                    for line in file.readlines():
                        content += line
            elif path.isfile(f'{all_path}index.htm'):
                with open(f'{all_path}index.htm', 'r') as file:
                    for line in file.readlines():
                        content += line
            else:
                routes = BrowsingFolder()
                html = routes.create_html(all_path)
                content = html

            return content
        raise Exception(400)

    def handle_response(self, message, body=''):
        response = f'HTTP/1.1 {message}\n\n{body}'
        self.sender.sendall(response.encode())

    @staticmethod
    def get_message(status_code: str):
        msg = '500 Internal Server Error'

        if '200' in status_code:
            msg = '200 OK'
        elif '400' in status_code:
            msg = '400 Bad Request'
        elif '404' in status_code:
            msg = '404 Not Found'
        elif '505' in status_code:
            msg = '505 Version Not Supported'

        return msg

    @staticmethod
    def handle_file(file_name: str):
        content = ''
        with open(file_name) as file:
            for line in file.readlines():
                content += line
        return content

    @staticmethod
    def handle_version(version: str):
        if '1.1' not in version:
            raise Exception(505)


class ServerTPC:
    def __init__(self, address, port):
        socket_server = socket(AF_INET, SOCK_STREAM)
        socket_server.bind((address, port))
        socket_server.listen()

        print(f'server is running at {address}:{port}')

        try:
            while True:
                (client_socket, client_address) = socket_server.accept()
                Thread(target=self.handle_data, args=(
                    client_socket, client_address)).start()
        except:
            socket_server.close()
            print('Server closed')

    @staticmethod
    def handle_data(client_socket: socket, client_address):
        while True:
            try:
                print(f'Client connected: {client_address}')
                data = client_socket.recv(2048)
                protocol = ProtocolHTTP(client_socket)
                protocol.handle_http(data.decode())
                # client_socket.close()
            except:
                client_socket.close()
                print(f'Connection with {client_address} was closed')


if __name__ == '__main__':
    ipaddress = input('Address: ')
    port = int(input('Port: '))
    server = ServerTPC(ipaddress, port)

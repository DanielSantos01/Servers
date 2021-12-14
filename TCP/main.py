from os import path
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import mimetypes
from BrowsingFolder import BrowsingFolder


class ProtocolHTTP:
    def __init__(self, sender):
        self.sender = sender

    @staticmethod
    def get_full_path(requested_path: str):
        file_path = requested_path

        if '/' == file_path:
            return 'files/'

        if requested_path[len(requested_path) - 1] != '/' and '.' not in requested_path:
            file_path += '/'

        return f'files/{file_path}'

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

            requested_path = self.get_full_path(requested_file)
            content, file_path = self.handle_method(
                http_method, requested_path)

            msg = self.get_message('200')
            self.handle_response(msg, content, file_path)

        except Exception as e:
            msg = self.get_message(repr(e))
            self.handle_response(msg, '<h1>NOT FOUND</h1>')

    @staticmethod
    def handle_method(method: str, all_path: str):
        if 'GET' in method:
            content = ''
            file_path = ''

            if path.isfile(all_path):
                file_path = all_path
                try:
                    with open(all_path, 'r') as file:
                        for line in file.readlines():
                            content += line
                except UnicodeDecodeError:
                    binary_file = open(all_path, 'rb')
                    content = binary_file.read()
                    binary_file.close()

            elif path.isfile(f'{all_path}index.html'):
                file_path = f'{all_path}index.html'
                with open(f'{all_path}index.html', 'r') as file:
                    for line in file.readlines():
                        content += line

            elif path.isfile(f'{all_path}index.htm'):
                file_path = f'{all_path}index.htm'
                with open(f'{all_path}index.htm', 'r') as file:
                    for line in file.readlines():
                        content += line
            elif path.isdir(all_path):
                routes = BrowsingFolder()
                html = routes.create_html(all_path)
                content = html
            else:
                raise Exception(404)

            return content, file_path
        raise Exception(400)

    def handle_response(self, message, body='', file_path=''):
        now = datetime.now()
        stamp = mktime(now.timetuple())
        date = format_date_time(stamp)
        if file_path == '':
            mime = 'text/html'
        else:
            mime = mimetypes.guess_type(file_path)
            mime = mime[0]

        response = f'HTTP/1.1 {message}\nDate: {date}\nServer: SocketTCP/1.0.0\ncontent-type: {mime}\n\n'
        if isinstance(body, bytes):
            data = body
        else:
            data = body.encode()
        self.sender.sendall(response.encode() + data)

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
    def __init__(self, address, socket_port):
        socket_server = socket(AF_INET, SOCK_STREAM)
        socket_server.bind((address, socket_port))
        socket_server.listen()

        print(f'server is running at {address}:{socket_port}')

        try:
            while True:
                (client_socket, client_address) = socket_server.accept()
                Thread(target=self.handle_data, args=(
                    client_socket, client_address)).start()
        finally:
            socket_server.close()
            print('Server closed')

    @staticmethod
    def handle_data(client_socket: socket, client_address):
        try:
            print(f'Client connected: {client_address}')
            data = client_socket.recv(4096)
            protocol = ProtocolHTTP(client_socket)
            protocol.handle_http(data.decode())
        finally:
            client_socket.close()
            print(f'Connection with {client_address} was closed')


if __name__ == '__main__':
    ipaddress = input('Address: ')
    port = int(input('Port: '))
    server = ServerTPC(ipaddress, port)

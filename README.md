# Servers Repository
Repository for the project of the Computers Networks course, containing servers in TCP and UDP architecture.
Both servers were developed by using the native python servers module*


### TCP server description
The TCP server can be runned by executing the ```/TCP/main.py``` file.<br />When running, the application will ask for an IP address and a port so it can run in it.<br />

### TCP server purpose
The purpose of the TCP server is to deviler files requested to the server. By accessing the ```/files/{file_name.extension}``` ou will be able to get the file (if it exists).

### UDP server description
The UDP application have its execution splitted in two parts:
- First, you can run the server by executing the ```/UDP/server.py``` file. So it will be waiting for UDP connections in the ```http://localhost:8080``` address.
- Then, you can run the client by executing the ```/UDP/client.py``` file, so ir can stablish a connection with the server by accessing its address.

### UDP server purpose
The purpose of the UDP server is to manage a quiz game. The game is multiplayer based, which means that you have to run (at least) two clients. Once the client is running, you will get all required information to play the game via terminal.

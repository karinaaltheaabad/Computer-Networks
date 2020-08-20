#######################################################################
# File:             server.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template server class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and add yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################
from builtins import object
import socket
import pickle
import threading
from client_handler import ClientHandler


class Server(object):
    MAX_NUM_CONN = 10

    def __init__(self, ip_address='127.0.0.1', port=12005):
        """
        Class constructor
        :param ip_address:
        :param port:
        """
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip_address = ip_address
        self.port = port
        self.clients = {}
        self.serversocket.bind((ip_address, port))

    def _listen(self):
        """
        Private method that puts the server in listening mode
        If successful, prints the string "Listening at <ip>/<port>"
        i.e "Listening at 127.0.0.1/10000"
        :return: VOID
        """
        try:
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Server running and listening at " + self.ip_address + "/" + str(self.port))
            print("Waiting for connections...")
        except:
            print("Error connecting to server")

    def _accept_clients(self):
        """
        # Handle client connections to the server
        :return: VOID
        """
        while True:
            try:
                clienthandler, addr = self.serversocket.accept()
                threading.Thread(target=self.client_handler_thread, args=(clienthandler, addr)).start()
            except:
                # handle exceptions here
                print("error accepting clients")

    def send(self, clientsocket, data):
        """
        Serializes the data with pickle, and sends using the accepted client socket.
        :param clientsocket:
        :param data:
        :return:
        """
        serialized_data = pickle.dumps(data)
        clientsocket.send(serialized_data)

    def receive(self, clientsocket, MAX_BUFFER_SIZE=4096):
        """
        Deserializes the data with pickle
        :param clientsocket:
        :param MAX_BUFFER_SIZE:
        :return: the deserialized data
        """
        raw_data = clientsocket.recv(MAX_BUFFER_SIZE)
        return pickle.loads(raw_data)

    def send_client_id(self, clientsocket, id):
        """
        Already implemented for you
        :param clientsocket:
        :return:
        """
        clientid = {'clientid': id}
        self.send(clientsocket, clientid)

    def client_handler_thread(self, clientsocket, address):
        """
        Sends the client id assigned to this clientsocket and
        Creates a new ClientHandler object
        See also ClientHandler Class
        :param clientsocket:
        :param address:
        :return: a client handler object.
        """
        print(f"Client {address} connected.")
        client_id = address[1]
        client_handler = ClientHandler(self, clientsocket, address)
        client_handler.run()
        self.clients[client_id] = client_handler
        return client_handler

    def run(self):
        """
        Already implemented for you. Runs this client
        :return: VOID
        """
        self._listen()
        self._accept_clients()


if __name__ == '__main__':
    server = Server()
    server.run()

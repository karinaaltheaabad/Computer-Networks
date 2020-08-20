########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: TCP Server Socket
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Karina Abad
# Student ID: 918533530
# Student Github Username:
# Lab Instructions: No partial credit will be given in this lab
# Program Running instructions: python3 server.py # compatible with python version 3
#
########################################################################################################################

# don't modify this imports.
import socket
import pickle
import threading
from threading import Thread
from client_handler import ClientHandler

class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10  # keeps 10 clients in queue

    def __init__(self, host="127.0.0.1", port=12000):
        """
        Class constructors
        :param host: by default localhost. Note that '0.0.0.0' takes LAN ip address.
        :param port: by default 12000
        """
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create server socket
        self.client_handlers = {}
        self.write_lock = threading.Lock()  # creates the lock
        self.write_lock.acquire()
        self.write_lock.release()  # lock is released

    def _bind(self):
        """
        # bind host and port to this server socket
        :return: VOID
        """
        self.serversocket.bind((self.host, self.port))

    def _listen(self):
        """
        # puts the server in listening mode.
        # if succesful, print the message "Server listening at ip/port"
        :return: VOID
        """
        try:
            self._bind()
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Listening at " + self.host + "/" + str(self.port))
            # your code here
        except:
            print("server refused connection")

    def threaded_client(self, clienthandler, addr):
        client_id = addr[1]
        client_handler = ClientHandler(self, clienthandler, addr)
        client_handler.run()
        self.client_handlers[client_id] = client_handler

    def _accept_clients(self):
        """
        # Handle client connections to the server
        :return: VOID
        """
        while True:
            try:
                clienthandler, addr = self.serversocket.accept()
                # from the addr variable, extract the client id assigned to the client
                threading.Thread(target=self.threaded_client, args=(clienthandler, addr)).start()
                print("Thread connected")
            except:
                # handle exceptions here
                print("error accepting clients")

    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """
        self._listen()
        self._accept_clients()


# main execution
if __name__ == '__main__':
    server = Server()
    server.run()

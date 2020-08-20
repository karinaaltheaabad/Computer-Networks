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
from threading import Thread


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
        Class constructor
        :param host: by default localhost. Note that '0.0.0.0' takes LAN ip address.
        :param port: by default 12000
        """
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create server socket

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
            self.serversocket.close()

    def _handler(self, clienthandler):
        """
        # receive, process, send response to the client using this handler.
        :param clienthandler:
        :return:
        """
        while True:
            # receive data from client
            # if no data, break the loop
            # Otherwise, send acknowledge to client. (i.e a message saying 'server got the data
            if self.receive(clienthandler):
                print("server got the data")
            else:
                break

            #  pass  remove this line after implemented.

    def _accept_clients(self):
        """
        # Handle client connections to the server
        :return: VOID
        """
        while True:
            try:
                clienthandler, addr = self.serversocket.accept()
                # from the addr variable, extract the client id assigned to the client
                client_id = {'clientid': addr[1]}
                # send assigned id to the new client. hint: call the send_clientid(..) method
                self._send_clientid(clienthandler, client_id)
                self._handler(clienthandler)  # receive, process, send response to client.
            except:
                # handle exceptions here
                print("error somewhere")

    def _send_clientid(self, clienthandler, clientid):
        """
        # send the client id to a client that just connected to the server.
        :param clienthandler:
        :param clientid:
        :return: VOID
        """
        self.send(clienthandler, clientid)

    def send(self, clienthandler, data):
        """
        # Serialize the data with pickle.
        # call the send method from the clienthandler to send data
        :param clienthandler: the clienthandler created when connection was accepted
        :param data: raw data (not serialized yet)
        :return: VOID
        """
        serialized_data = pickle.dumps(data)  # creates a stream of bytes
        clienthandler.send(serialized_data)

    def receive(self, clienthandler, MAX_ALLOC_MEM=4096):
        """
        # Deserialized the data from client
        :param MAX_ALLOC_MEM: default set to 4096
        :return: the deserialized data.
        """
        raw_data = clienthandler.recv(MAX_ALLOC_MEM)  # receives data from this client
        data = pickle.loads(raw_data)  # deserializes the data from the client
        return data  # change the return value after implemented.

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

#######################################################################
# File:             client.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template client class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and add yours instead.
# Running:          Python 2: python client.py
#                   Python 3: python3 client.py
#
########################################################################
import pickle
import socket


class Client(object):
    """
    The client class provides the following functionality:
    1. Connects to a TCP server
    2. Send serialized data to the server by requests
    3. Retrieves and deserialize data from a TCP server
    """

    def __init__(self):
        """
        Class constructor
        """
        # Creates the client socket
        # AF_INET refers to the address family ipv4.
        # The SOCK_STREAM means connection oriented TCP protocol.
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip_address, port):
        """
        Connects to a server. Implements exception handler if connection is reset.
	    Then retrieves the cliend id assigned from server, and sets
        :param host:
        :param port:
        :return: VOID
        """
        self.clientSocket.connect((ip_address, port))
        # print("Successfully connected to server at " + ip_address + "/" + str(port))
        data = self.receive()
        client_id = data['clientid']
        server_addr = data['serverip']
        self.server_address = server_addr
        self.client_id = client_id
        # print("Client id " + str(self.client_id) + " connected to peer " + str(self.server_address))
        while True:
            try:
                data = self.receive()
                if not data:
                    break
                if data:
                    print(data)
            except Exception as error:
                print(error)
                print("error there")
        self.close()

    def send(self, data):
        """
        Serializes and then sends data to server
        :param data:
        :return:
        """
        data = pickle.dumps(data)  # serialized data
        self.clientSocket.send(data)

    def receive(self, MAX_BUFFER_SIZE=4090):
        """
        Deserializes the data received by the server
        :param MAX_BUFFER_SIZE: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        raw_data = self.clientSocket.recv(MAX_BUFFER_SIZE)  # deserializes the data from server
        return pickle.loads(raw_data)

    def bind(self, host, port):
        self.clientSocket.bind((host, port))

    def close(self):
        """
        close the client socket
        :return: VOID
        """
        self.clientSocket.close()

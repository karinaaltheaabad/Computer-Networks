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
from menu import Menu

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
        self.clientid = 0

    def connect(self):
        """
        Connects to a server. Implements exception handler if connection is reset.
	    Then retrieves the cliend id assigned from server, and sets
        :param host: 
        :param port: 
        :return: VOID
        """
        self.host = input("Enter the server IP Address: ")
        self.port = int(input("Enter the server port: "))
        self.key = input("Your id key (i.e your name): ")
        self.clientSocket.connect((self.host, self.port))
        keys = {'client_key': self.key}
        self.send(keys)
        print("Successfully connected to server at " + self.host + "/" + str(self.port))
        print("Your client info is: \nUsername: " + self.get_key() + "\nClient id: " + str(self.get_client_id()))

        while True:  # client is put in listening mode to retrieve data from server.
            menu = Menu()
            menu.process_user_data()
            if not menu:
                break
        self.close()

    def get_key(self):
        return self.key

    def get_client_id(self):
        data = self.receive()  # deserialized data
        client_id = data['clientid']  # extracts client id from data
        self.client_id = client_id  # sets the client id to this client
        return client_id

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

    def close(self):
        """
        close the client socket
        :return: VOID
        """
        self.clientSocket.close()


if __name__ == '__main__':
    client = Client()
    client.connect()

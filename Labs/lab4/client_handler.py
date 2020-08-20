########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: Server support for multiple clients
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Karina Abad
# Student ID: 918533530
# Student Github Username: karinaaltheaabad
# Lab Instructions: No partial credit will be given. Labs must be completed in class, and must be committed to your
#               personal repository by 9:45 pm.
# Running instructions: This program needs the server to run. The server creates an object of this class.
#
########################################################################################################################

import threading
import pickle


class ClientHandler:
    """
    The client handler class receives and process client requests
    and sends responses back to the client linked to this handler.
    """

    def __init__(self, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you.
        :param server_instance: passed as 'self' when the object of this class is created in the server object
        :param clientsocket: the accepted client on server side. this handler, by itself, can send and receive data
                             from/to the client that is linked to.
        :param addr: addr[0] = server ip address, addr[1] = client id assigned buy the server
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.handler = clientsocket
        self.print_lock = threading.Lock()  # creates the print lock

    def process_client_data(self):
        """
        receives the data from the client
        prepares the data to be printed in console
        acquire the print lock
        prints the data in server console
        release the print lock
        keep this handler object listening for more incoming data from the client
        :return: VOID
        """
        try:
            self._send_clientid(self.client_id)
            data = self.receive()
            while True:
                if not data:
                    break
                self.print_lock.acquire()
                print("--server got the data--")
                print(data)
                self.print_lock.release()
                data = self.receive()
        except:
            pass

    def _send_clientid(self, clientid):
        """
        # send the client id to a client that just connected to the server.
        :param clienthandler:
        :param clientid:
        :return: VOID
        """
        client_id = {'clientid': clientid}
        self.send(client_id)

    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.handler.send(serialized_data)

    def receive(self, max_mem_alloc=4096):
        raw_data = self.handler.recv(max_mem_alloc)
        data = pickle.loads(raw_data)
        return data

    def run(self):
        self.process_client_data()

#######################################################################
# File:             client_handler.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template ClientHandler class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client handler class, and use a version of yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################
import pickle
import threading
from menu import Menu


class ClientHandler(object):
    """
    The ClientHandler class provides methods to meet the functionality and services provided
    by a server. Examples of this are sending the menu options to the client when it connects,
    or processing the data sent by a specific client to the server.
    """

    def __init__(self, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you
        :param server_instance: normally passed as self from server object
        :param clientsocket: the socket representing the client accepted in server side
        :param addr: addr[0] = <server ip address> and addr[1] = <client id>
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.clientsocket = clientsocket
        self.server.send_client_id(self.clientsocket, self.client_id)
        self.unread_messages = []
        self.print_lock = threading.Lock()
        # self.key_list = self.receive(self.clientsocket)['client_key']

    def _sendMenu(self):
        """
        Already implemented for you.
        sends the menu options to the client after the handshake between client and server is done.
        :return: VOID
        """
        menu = Menu()
        data = {'menu': menu}
        self.server.send(self.clientsocket, data)

    def run(self):
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
        self.clientsocket.send(serialized_data)

    def receive(self, max_mem_alloc=4096):
        raw_data = self.clientsocket.recv(max_mem_alloc)
        data = pickle.loads(raw_data)
        return data

    def process_options(self):
        """
        Process the option selected by the user and the data sent by the client related to that
        option. Note that validation of the option selected must be done in client and server.
        In this method, I already implemented the server validation of the option selected.
        :return:
        """
        data = self.server.receive(self.clientsocket)
        if 'option_selected' in data.keys() and 1 <= data['option_selected'] <= 6:  # validates a valid option selected
            option = data['option_selected']
            if option == 1:
                self._send_user_list()
            elif option == 2:
                recipient_id = data['recipient_id']
                message = data['message']
                self._save_message(recipient_id, message)
            elif option == 3:
                self._send_messages()
            elif option == 4:
                room_id = data['room_id']
                self._create_chat(room_id)
            elif option == 5:
                room_id = data['room_id']
                self._join_chat(room_id)
            elif option == 6:
                self._disconnect_from_server()
        else:
            print("The option selected is invalid")

    def _send_user_list(self):
        """
         send the list of users (clients ids) that are connected to this server.
        :return: VOID
        """
        client_list = {}
        for i in self.server.clients:
            client_list[self.server.clients[i].name] = str(self.server.clients[i].client_id)
        self.server.send(self.clientsocket, client_list)

    def _save_message(self, recipient_id, message):
        """
        link and save the message received to the correct recipient. handle the error if recipient was not found
        :param recipient_id:
        :param message:
        :return: VOID
        """
        messages = []
        try:
            if recipient_id:
                messages.append(message)
        except:
            print("Recipient not found")

    def _send_messages(self):
        """
        send all the unread messages of this client. if non unread messages found, send an empty list.
        make sure to delete the messages from list once the client acknowledges that they were read.
        :return: VOID
        """
        if len(self.unread_messages) > 0:
            self.clientsocket.send(self.unread_messages)
            if self.clientsocket.recv(self.unread_messages):
                for i in self.unread_messages:
                    self.unread_messages.pop(i)
        else:
            self.clientsocket.send(self.unread_messages)

    def _create_chat(self, room_id):
        """
        Creates a new chat in this server where two or more users can share messages in real time.
        :param room_id:
        :return: VOID
        """
        id_list = []
        id = input("Create chat ID: ")
        if id_list.__contains__(id):
            print("ID already taken.")
            id = input("Create chat ID: ")

    def _join_chat(self, room_id):
        """
        TODO: join a chat in a existing room
        :param room_id:
        :return: VOID
        """

        pass

    def delete_client_data(self):
        """
        delete all the data related to this client from the server.
        :return: VOID
        """
        for client in self.server.clients:
            self.server.clients.pop(client)

    def _disconnect_from_server(self):
        """
        call delete_client_data() method, and then, disconnect this client from the server.
        :return: VOID
        """
        self.delete_client_data()
        self._disconnect_from_server()

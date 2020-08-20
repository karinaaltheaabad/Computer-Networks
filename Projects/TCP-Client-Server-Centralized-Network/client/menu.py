#######################################################################################
# File:             menu.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assignment #1 TCP socket programming
# Description:      Template Menu class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this Menu class, and use a version of yours instead.
# Important:        The server sends a object of this class to the client, so the client is
#                   in charge of handling the menu. This behavior is strictly necessary since
#                   the client does not know which services the server provides until the
#                   clients creates a connection.
# Running:          This class is dependent of other classes.
# Usage :           menu = Menu() # creates object
#
########################################################################################


class Menu(object):
    """
    This class handles all the actions related to the user menu.
    An object of this class is serialized ans sent to the client side
    then, the client sets to itself as owner of this menu to handle all
    the available options.
    Note that user interactions are only done between client and user.
    The server or client_handler are only in charge of processing the
    data sent by the client, and send responses back.
    """

    def __init__(self, client=None):
        """
        Class constractor
        :param client: the client object on client side
        """
        self.client = client

    def set_client(self, client):
        self.client = client

    def show_menu(self):
        """
        send a request to server requesting the menu.
        receive and process the response from server (menu object) and set the menu object to self.menu
        print the menu in client console.
        :return: VOID
        """
        menu = self.get_menu()
        print(menu)

    def process_user_data(self):
        """
        according to the option selected by the user, prepare the data that will be sent to the server.
        :param option:
        :return: VOID
        """
        self.show_menu()
        option = self.option_selected()
        if 1 <= option <= 6:  # validates a valid option
            # (i,e  algo: if option == 1, then data = self.menu.option1, then. send request to server with the data)
            if option == 1:
                data = self.option1()
                # self.client.send(data)
                # keys = self.client.receive()
                # for i in keys:
                #     print("User id: " + keys[i] + "client name: " + keys[i])
            elif option == 2:
                data = self.option2()
                self.client.send(data)

    def option_selected(self):
        """
        :return: the option selected.
        """
        option = int(input("Your option <enter a number>: "))
        return option

    def get_menu(self):
        """
        Implement the following menu
        ****** TCP CHAT ******
        -----------------------
        Options Available:
        1. Get user list
        2. Sent a message
        3. Get my messages
        4. Create a new channel
        5. Chat in a channel with your friends
        6. Disconnect from server
        :return: a string representing the above menu.
        """
        menu = """
                ****** TCP CHAT ******
        -----------------------
        Options Available:
        1. Get user list
        2. Sent a message
        3. Get my messages
        4. Create a new channel
        5. Chat in a channel with your friends
        6. Disconnect from server
        """
        return menu

    def option1(self):
        """
        :param option:
        :return: a python dictionary with all the data needed from user in option 1.
        """
        data = {}
        data['option'] = 1
        return data

    def option2(self):
        """
        :param option:
        :return: a python dictionary with all the data needed from user in option 2.
        """
        data = {}
        data['option'] = 2
        # Your code here.
        return data

    def option3(self):
        """
        :param option:
        :return: a python dictionary with all the data needed from user in option 3.
        """
        data = {}
        data['option'] = 3
        # Your code here.
        return data

    def option4(self):
        """
        :param option:
        :return: a python dictionary with all the data needed from user in option 4.
        """
        data = {}
        data['option'] = 4
        # Your code here.
        return data

    def option5(self):
        """
        :param option:
        :return: a python dictionary with all the data needed from user in option 5.
        """
        data = {}
        data['option'] = 5
        # Your code here.
        return data

    def option6(self):
        """
        :param option:
        :return: a python dictionary with all the data needed from user in option 6.
        """
        data = {}
        data['option'] = 6
        # Your code here.
        return data

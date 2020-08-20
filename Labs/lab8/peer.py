"""
Lab 8: peer.py
This file contains a basic template of the Peer class. In this lab, your job 
is to implement all the parts marked as TODO.
Note that you don´t need to run the code of this lab. The goal of this lab is to see how your logic works, and
therefore, to make sure that you understood how peers perform the downloading 
and uploading process in the network, and also which challenges you may encounter
when implementing those functionality.
"""
from server import Server  # assumes that your server file is in this folder
from client import Client  # assumes that your client file is in this folder
from tracker import Tracker  # assumes that your Tracker file is in this folder
import uuid
import threading
import downloader
import pwp
import torrent


class Peer:
    SERVER_PORT = 4977
    CLIENT_MIN_PORT_RANGE = 5001
    CLIENT_MAX_PORT_RANGE = 5010
    MAX_NUM_CONNECTIONS = 10
    MAX_UPLOAD_RATE = 100  # BITS PER SECOND
    MAX_DOWNLOAD_RATE = 1000  # BITS PER SECOND

    PEER = 'peer'
    SEEDER = 'seeder'

    def __init__(self, role=SEEDER):
        self.role = role
        self.id = uuid.uuid4()
        self.server = Server(port=self.SERVER_PORT)
        self.tracker = Tracker('age.torrent', self.server, self.id)
        self.pwp = pwp.PWP
        self.torrent = torrent.Torrent('age.torrent')

    def run_server(self):
        """
         * Create and run a threaded server object
              * Every time the server accepts a client, the server must create a threaded uploader object
              * The uploader object is similar to the client-handler in your TCP Client-Assignment. It handles
                communication processes between the uploader and the downloader
        """
        try:
            threading.Thread(target=self.server.run).start()
            print("Thread server connected")
        except Exception as error:
            # handle exceptions here
            print(error)

    def run_tracker(self):
        """
        TODO: 1. Create and run a threaded tracker
        :param server: the server instance.
        """
        try:
            threading.Thread(target=self.tracker.run).start()
            print("Thread tracker connected")
        except Exception as error:
            print(error)

    def interested(self):
        interested = self.pwp.message(self.pwp.INTERESTED)
        return interested

    def non_interested(self):
        non_interested = self.pwp.message(self.pwp.NOT_INTERESTED)
        return non_interested

    def _connect_to_peer(self, client_port_to_bind, peer_ip_address, peer_port=SERVER_PORT, interested=True,
                         keep_alive=True):
        """
        * Create a new client object and bind the port given as a
              parameter to that specific client. Then use this client
              to connect to the peer (server) listening in the ip
              address provided as a parameter
              * Thread the client
              * Run the downloader

        :param client_port_to_bind: the port to bind to a specific client
        :param peer_ip_address: the peer ip address that
                                the client needs to connect to
        :return: VOID
        """
        client = Client()
        try:
            client.bind('127.0.0.1', client_port_to_bind)
            threading.Thread(target=client.connect, args=(peer_ip_address, peer_port)).start()
            downloader.Downloader(client, self.id, self.torrent, self.pwp, interested, keep_alive).run()
            return True
        except Exception as error:
            print(error)
            print("error here")
            client.close()
            return False

    def connect(self, peers_ip_addresses):
        """
         Initialize a temporal variable to the min client port range, then
              For each peer ip address, call the method _connect_to_peer()
              method, and then increment the client´s port range that
              needs to be bind to the next client. Break the loop when the
              port value is greater than the max client port range.

        :param peers: list of peer´s ip addresses in the network
        :return: VOID
        """
        client_port = self.CLIENT_MIN_PORT_RANGE
        default_port = self.SERVER_PORT
        for peeer in peers_ip_addresses:
            if "/" in peeer:
                split = peeer.split("/")
                peeer = split[0]
                default_port = int(split[1])
            if self._connect_to_peer(client_port, peeer, default_port):
                client_port += 1


peer = Peer(role='peer')
print("Peer: " + str(peer.id) + " running its server: ")
peer.run_server()
peer.run_tracker()

if peer.role == peer.PEER:
    peer_ips = ['127.0.0.1/5000', '127.0.0.1/4999']
    peer.connect(peer_ips)

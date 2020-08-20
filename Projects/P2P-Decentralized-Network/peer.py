from client import Client
from pwp import PWP
from server import Server
from torrent import Torrent
from tracker import Tracker
from config import Config
from downloader import Downloader
import threading
import uuid


# import bencode


class Peer:
    SERVER_PORT = 4977
    CLIENT_MIN_PORT_RANGE = 5001
    CLIENT_MAX_PORT_RANGE = 5010
    MAX_NUM_CONNECTIONS = 10
    MAX_UPLOAD_RATE = 100  # BITS PER SECOND
    MAX_DOWNLOAD_RATE = 1000  # BITS PER SECOND

    PEER = 'peer'
    SEEDER = 'seeder'

    def __init__(self, role=SEEDER, ip_address='127.0.0.1'):
        self.role = role
        self.id = uuid.uuid4()
        self.ip = ip_address
        self.server = Server(self.id, port=self.SERVER_PORT)
        self.tracker = Tracker('age.torrent', self.server, self.id)
        self.torrent = Torrent('age.torrent')
        self.pwp = PWP()
        self.pwp.msg.init_bitfield(8)
        self.bitfield = self.pwp.msg.get_bitfield()
        self.run_server()
        self.run_tracker()
        self.console_print()
        while True:
            continue

    def run_server(self):
        """
        * Create and run a threaded server object
              * Every time the server accepts a client, the server must create a threaded uploader object
            * The uploader object is similar to the client-handler in your TCP Client-Assignment. It handles
            communication processes between the uploader and the downloader
        """
        try:
            threading.Thread(target=self.server.run).start()
        except Exception as error:
            print(error)

    def run_tracker(self):
        """
        Create and run a threaded tracker
        :param server: the server instance.
        """
        try:
            threading.Thread(target=self.tracker.run).start()
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
        * Thread the client Run the downloader

        :param client_port_to_bind: the port to bind to a specific client
        :param peer_ip_address: the peer ip address that
                                    the client needs to connect to
        :return: VOID
            """
        client = Client()
        try:
            client.bind('127.0.0.1', client_port_to_bind)
            threading.Thread(target=client.connect, args=(peer_ip_address, peer_port)).start()
            Downloader(client, self.id, self.torrent, self.pwp, interested, keep_alive).run()
            return True
        except Exception as error:
            print(error)
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

    def console_print(self):
        print("\n\n***** P2P Client App *****")
        print("Peer id: " + str(self.id))
        print("Peer IP Address: 127.0.0.1")
        print("Tracker/s info: IP: " + self.torrent.announce() + "/" + str(5000))
        print("Max download rate: " + str(self.MAX_DOWNLOAD_RATE) + "b/s")
        print("Max upload rate: " + str(self.MAX_UPLOAD_RATE) + "b/s")
        print("\nTorrent: age.torrent")
        print("file: age.txt")
        print("seeder/s: " + self.torrent.announce() + "/" + str(self.SERVER_PORT))
        # self.decode_torrent()

    def decode_torrent(self):
        # bencoded = bencode.bdecode(open('age.torrent', 'rb').read())
        # print(bencoded)
        pass


peer = Peer(role='seeder')
print("Peer: " + str(peer.id) + " running its server: ")
peer.run_server()
peer.run_tracker()

if peer.role == peer.PEER:
    peer_ips = ['127.0.0.1/5000', '127.0.0.1/4999']
    peer.connect(peer_ips)

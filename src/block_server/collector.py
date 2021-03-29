import socket
from datetime import datetime
from block_core.blocked import Blocked
import threading

class Collector(threading.Thread):

    def __init__(self, cache):
        # Create a TCP/IP socket for receiving data
        RCV_UDP_IP = ''
        RCV_UDP_PORT = 5140

        # Bind the socket to the port
        self.rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rcv_sock.bind((RCV_UDP_IP, RCV_UDP_PORT))
        self.cache = cache

    def go(self):

        while True:
            # Receive message
            data, address = self.rcv_sock.recvfrom(1024)

            # Parse original message and create a new one
            (time_str, ip, protocol) = data.decode("utf-8").split(',')

            timestamp = datetime.strptime(time_str, '%Y/%m/%d %H:%M:%S')
            self.cache.add(Blocked(timestamp, ip, protocol))

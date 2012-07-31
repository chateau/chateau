#!/usr/bin/env python3

import socket, asynchat, asyncore, ssl

class Connection(asynchat.async_chat):
    def __init__(self, address, port, use_ssl, bot):
        asynchat.async_chat.__init__(self)
        self.ibuffer = b""
        self.address = address
        self.port = port
        self.use_ssl = use_ssl
        self.bot = bot
        self.set_terminator(b"\r\n")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            if use_ssl:
                try:
                    ssl_sock = ssl.wrap_socket(sock)
                    self.set_socket(ssl_sock)
                except ssl.SSLError as error:
                    raise error
            else:
                self.set_socket(sock)
        except socket.error as error:
            raise error

    def collect_incoming_data(self, data):
        self.ibuffer += data

    def start(self):
        self.connect((self.address, self.port))

    def handle_connect(self):
        self.bot.handle_connect()

    def found_terminator(self):
        data = self.ibuffer.decode("utf_8")
        self.ibuffer = b""
        self.bot.handle_line(data)
        
def loop():
    asyncore.loop()

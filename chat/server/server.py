#!/usr/bin/env python
# encoding: utf-8

import socket
import threading
import configparser

from chat.lib.logger import BaseLogger

log = BaseLogger().get_logger(__name__)

config = configparser.ConfigParser()
config.read("../config.ini")

ACCPET_NUM = config['SERVER'].getint('ACCEPT_NUM')
SERVER_IP = config['SERVER']['LOCAL_IP']
SERVER_PORT = config['SERVER'].getint('LOCAL_PORT')

SERVER_CONF = (SERVER_IP, SERVER_PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_CONF)

# listen 方法的参数会告诉套接字库，我们希望在队列中累积多达 5 个（通常的最大值）连接请求后再拒绝外部连接
server.listen(ACCPET_NUM)

class client_thread(threading.Thread):
    """
    :param client_skt:
    :return:
    """

    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        """
        接受消息
        :return:
        """
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            log.info("receive data from %s: %s" % (self.addr, data))


log.info("Server starting ......")

while True:
    # accept connections from outside
    (clientsocket, addr) = server.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server

    log.info("accept conn from %s:%s" % addr)
    ct = client_thread(clientsocket, addr)
    ct.run()


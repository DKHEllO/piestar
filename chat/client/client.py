#!/usr/bin/env python
# encoding: utf-8

import socket
import configparser
from datetime import datetime

config = configparser.ConfigParser()
config.read("../config.ini")

MSGLEN = config['CLIENT'].getint('MSG_LEN')
SERVER_IP = config['CLIENT']['SERVER_IP']
SERVER_PORT = config['CLIENT']['SERVER_PORT']
SERVER_CONF = (SERVER_IP, SERVER_PORT)

def display(msg):
    """
    输出消息附加当前时间
    :param msg:
    :return:
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    output_format = "[{time}] {msg}"
    print(output_format.format(time=now, msg=msg))

class ClientSocket:
    """"""
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        msg_len = len(msg)
        totalsent = 0
        while totalsent < msg_len:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("msg send failed: socket connection broken")
            totalsent = totalsent + sent
        display("msg sent: %s" % msg)

    def receive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

client = ClientSocket()

try:
    client.connect(*SERVER_CONF)
except Exception as e:
    display("conneting server %s error: %s" % (str(SERVER_CONF), str(e)))

while True:
    try:
        msg = input(">").strip()
        if msg:
            client.send(msg.encode("utf-8"))
    except Exception as e:
        display("send msg error: %s" % str(e))



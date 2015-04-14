from alchemy.network.nanolink import gate, push, pull
from alchemy.sdn.docker import dockersdn

from logbook import Logger
import socket

import hashlib


log = Logger("{host} - {service}".format(host=socket.gethostname(), service="Encryptor"))

def encryptor():
    plaintext = gate('in', network=dockersdn('plaintext'))
    encrypted = gate('out', network=dockersdn('encrypted'))

    while True:
        packet = pull(plaintext)
        epacket = hashlib.sha512(packet).hexdigest()
        push(epacket, encrypted)


if __name__ == '__main__':
  encryptor()

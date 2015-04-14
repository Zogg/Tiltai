from alchemy.network.nanolink import gate, push, pull
from alchemy.sdn.docker import dockersdn

import time
import socket

from logbook import Logger


log = Logger("{host} - {service}".format(host=socket.gethostname(), service="Feeder"))

def feeder():
    plaintext = gate('out', network=dockersdn('plaintext'))

    while True:
        log.debug("Sending message")
        push("Plaintext message", plaintext)
        time.sleep(3)

if __name__ == '__main__':
  feeder()

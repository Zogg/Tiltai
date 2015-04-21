from alchemy.network.nanolink import gate, push, pull
from alchemy.sdn.docker import dockersdn
from alchemy.sdn.consulregistrator import get_topology
from alchemy.sdn.consulregistrator import addr
from alchemy.control.network import routine


from functools import partial

import time
import socket

from logbook import Logger


log = Logger("{host} - {service}".format(host=socket.gethostname(), service="Feeder"))

def feeder():
    plaintext = gate('out', network=dockersdn('plaintext', resolver=addr, storage=get_topology), 
                            governor=partial(routine, resolver=partial(dockersdn, 'plaintext', addr, get_topology)))

    while True:
        log.debug("Sending message")
        push("Plaintext message", plaintext)
        time.sleep(3)

if __name__ == '__main__':
  feeder()

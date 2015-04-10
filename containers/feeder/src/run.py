from control import gate, push, pull
from control import dockersdn

import time
from datetime import datetime

from logbook import Logger

log = Logger("{host} - {service}".format(host=socket.gethostname(), service="Feeder"))

def feeder():
    plaintext = gate('out', network=dockersdn('plaintext'))

    while True:
        logging.debug("Sending message")
        push("Plaintext message", plaintext)
        time.sleep(3)

if __name__ == '__main__':
  feeder()

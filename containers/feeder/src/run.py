from control import gate, push, pull
from control import dockersdn

import time
from datetime import datetime

def feeder():
    plaintext = gate('out', network=dockersdn('plaintext'))

    while True:
        print(datetime.now(), "Sending message")
        push("Plaintext message", plaintext)
        time.sleep(3)

if __name__ == '__main__':
  feeder()

from control import gate, push, pull
from control import dockersdn

import hashlib


def encryptor():
    plaintext = gate('in', network=dockersdn('plaintext'))
    encrypted = gate('out', network=dockersdn('encrypted'))

    while True:
        packet = pull(plaintext)
        epacket = hashlib.sha512(packet).hexdigest()
        push(epacket, encrypted)


if __name__ == '__main__':
  encryptor()

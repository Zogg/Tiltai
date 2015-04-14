from alchemy.network.nanolink import gate, push, pull
from alchemy.sdn.docker import dockersdn

from logbook import Logger
import socket

log = Logger("{host} - {service}".format(host=socket.gethostname(), service="Email-Sink"))

def emailsink():
    crypted_mails = gate('in', network=dockersdn('crypted_mails'))

    while True:
        email = pull(crypted_mails)
        log.info(email)


if __name__ == '__main__':
  emailsink()

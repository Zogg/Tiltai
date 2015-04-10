from control import gate, push, pull
from control import dockersdn

from logbook import Logger

log = Logger("{host} - {service}".format(host=socket.gethostname(), service="Feeder"))

def emailsink():
    crypted_mails = gate('in', network=dockersdn('crypted_mails'))

    while True:
        email = pull(crypted_mails)
        log.info(email)


if __name__ == '__main__':
  emailsink()

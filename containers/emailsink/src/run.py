from control import gate, push, pull
from control import dockersdn

def emailsink():
    crypted_mails = gate('in', network=dockersdn('crypted_mails'))

    while True:
        email = pull(crypted_mails)
        print(email)


if __name__ == '__main__':
  emailsink()

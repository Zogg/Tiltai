from control import gate, push, pull
from nanomsg import PUSH, PULL, PUB, SUB

from consullib import addr

import hashlib
import threading
import time

    
def encryptor():
    emails = gate('in', network={'port': 4567, 'type': PULL})
    crypted_mails = gate('out', network={'port': 5678})
    
    while True:
        email = pull(emails)
        encryptedemail = hashlib.sha512(email).hexdigest()
        push(encryptedemail, crypted_mails)
        
def emailsink():
    crypted_mails = gate('in', network={'port': 5678, 'type': PULL})

    while True:
        email = pull(crypted_mails)
        print(email)

def feeder():
    plaintext = gate('out', network={'port': 4567, 'type': PUSH})

    for i in range(3):
        print("Sending message")
        push("Plaintext message", plaintext)
        time.sleep(3)

        
t2 = threading.Thread(target=feeder)
t3 = threading.Thread(target=encryptor)
t4 = threading.Thread(target=emailsink)

threads = [t2,t3,t4]
for thread in threads:
    thread.start()


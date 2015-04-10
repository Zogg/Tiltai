from nanomsg import Socket, PUSH, PULL, PUB, SUB, SUB_SUBSCRIBE

import Queue
import threading


subbed_topics = []

def receiver(queue, ports, stype=SUB):
    in_sock = Socket(stype)
    
    for port in ports:
      in_sock.bind('tcp://0.0.0.0:{port}'.format(port=port))
    
    def receive_messages():
        while True:
            queue.put(in_sock.recv())
            print("Message received")

    receiver = threading.Thread(target=receive_messages)
    receiver.start()
    
    return in_sock

def sender(queue, endnodes, stype=PUSH):
    out_sock = Socket(stype)
    
    for node in endnodes:
      out_sock.connect('tcp://{ip}:{port}'.format(ip=node['ip'], 
                                                  port=node['port']))
    
    def send_messages():
        while True:
            out_sock.send(queue.get(block=True))
            print("Message has been sent")

    receiver = threading.Thread(target=send_messages)
    receiver.start()
    
    return out_sock

def gate(type, queue=Queue.Queue(), network={}):
    if type == 'out':
        sender(queue, network, stype=network.get('type', PUSH))
    elif type == 'in':
        receiver(queue, network['ports'], stype=network.get('type', SUB))
    elif type == 'utility':
        pass
    else:
        raise ValueError("No such gate type known.")
        return Null
    
    return queue

def topic(sock, topic=None):
    if topic not in subbed_topics:
        sock.set_string_option(SUB, SUB_SUBSCRIBE, topic)
        subbed_topics.append(topic)

def pull(queue):
    return queue.get(block=True)

def push(message, queue):
    queue.put(message)

class PushPull():
    def __init__(self, pull='in_', push='out_'):
        emails = Queue.Queue()
        incoming = receiver(emails, 4567, stype=PULL)

        crypted_mails = Queue.Queue()
        outgoing = sender(crypted_mails, 5678)
    
    def __call__(self):
        pass

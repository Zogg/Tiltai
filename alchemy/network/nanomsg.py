from nanomsg import Socket, PUSH, PULL, PUB, SUB, SUB_SUBSCRIBE, PAIR, SOL_SOCKET, SNDTIMEO, NanoMsgAPIError

import threading

from logbook import Logger

log = Logger("{host} - {service}".format(host=socket.gethostname(), service="Feeder"))


sock_type = {'PUSH': PUSH,
             'PULL': PULL,
             'PUB': PUB,
             'SUB': SUB,
             'PAIR': PAIR}

subbed_topics = []

out_endpoints = []
in_endpoints = []


def receiver(queue, ports, stype=SUB):
    in_sock = Socket(stype)
    
    for port in ports:
      in_sock.bind('tcp://0.0.0.0:{port}'.format(port=port))
    
    def receive_messages():
        while True:
            queue.put(in_sock.recv())
            log.info("Message received")

    receiver = threading.Thread(target=receive_messages)
    receiver.start()
    
    return in_sock

def sender(queue, network, stype=PUSH):
    out_sock = Socket(stype)
    
    out_sock.set_int_option(SOL_SOCKET, SNDTIMEO, 1000)
    
    for node in network['nodes']:
        endpoint = out_sock.connect('tcp://{ip}:{port}'.format(ip=node['ip'], 
                                                               port=node['port']))
        out_endpoints.append(endpoint)
      
    def send_messages():
        while True:
            try:
                out_sock.send(queue.get(block=True))
                log.info("Message has been sent")
            except NanoMsgAPIError as e:
                log.debug(e)
                log.debug(dir(e))
                

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

def igate(queue=Queue.Queue(), network={}):
  return gate('in', queue, network)

def ogate(queue=Queue.Queue(), network={}):
  return gate('out', queue, network) 

def iogate(type, queuein=Queue.Queue(), queueout=Queue.Queue(), network={}):
    sock = Socket(network['type'])
    
    if type == 'in':
      for port in network['ports']:
        sock.bind('tcp://0.0.0.0:{port}'.format(port=port))
    elif type == 'out':
      for node in network['nodes']:
        sock.connect('tcp://{ip}:{port}'.format(ip=node['ip'], 
                                                port=node['port']))
        
    def receive_messages():
        while True:
            queuein.put({'socket':in_sock, 'data': in_sock.recv()})
            log.info("Message received")
            
    def send_messages():
        while True:
            sock.send(queueout.get(block=True))
            log.info("Message has been sent")

    receiver = threading.Thread(target=receive_messages)
    sender = threading.Thread(target=send_messages)
    receiver.start()
    sender.start()
    
    return (queuein, queueout)

  
def topic(sock, topic=None):
    if topic not in subbed_topics:
        sock.set_string_option(SUB, SUB_SUBSCRIBE, topic)
        subbed_topics.append(topic)
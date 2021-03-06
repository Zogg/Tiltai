from nanomsg import Socket, PUSH, PULL, PUB, SUB, SUB_SUBSCRIBE, PAIR

import Queue
import threading


sock_type = {'PUSH': PUSH,
             'PULL': PULL,
             'PUB': PUB,
             'SUB': SUB,
             'PAIR': PAIR}

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

def sender(queue, network, stype=PUSH):
    out_sock = Socket(stype)

    for node in network['nodes']:
      print('tcp://{ip}:{port}'.format(ip=node['ip'], 
                                                  port=node['port']))
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
            print("Message received")
            
    def send_messages():
        while True:
            sock.send(queueout.get(block=True))
            print("Message has been sent")

    receiver = threading.Thread(target=receive_messages)
    sender = threading.Thread(target=send_messages)
    receiver.start()
    sender.start()
    
    return (queuein, queueout)

  
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

#        
# SDN
#

def dockersdn(queue_name):
  """whoami"""
  from consullib import addr
  import socket
  hostname = socket.gethostname()
  print(hostname)
  import aerospike
  config = {
    'hosts': [
        ( '172.17.42.1', 3000 )
    ],
    'policies': {
        'timeout': 1000 # milliseconds
    }
  }
  client = aerospike.client(config)
  client.connect()

  key = ('sdn', 'service', hostname)
  (key, meta, links) = client.select(key, ['links'])

  if links:
    for link in links['links']:
      if link['queue'] == queue_name:
        if link.get('outgate', None):
          nodes = {'nodes': addr(link['outgate'])}
        else:
          nodes = {'ports': link.get('ports', [])}
                  
        if link.get('type', None):
          nodes['type'] = sock_type[link['type']]
        
        print(nodes)
        return nodes

  return {'nodes': []}

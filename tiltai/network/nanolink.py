from nanomsg import Socket, PUSH, PULL, PUB, SUB, SUB_SUBSCRIBE, PAIR, SOL_SOCKET, SNDTIMEO, NanoMsgAPIError
from nanomsg import wrapper as nn_wrapper

import threading
import Queue
import socket

from logbook import Logger

log = Logger("{host} - {service}".format(host=socket.gethostname(), service="nanolink"))


sock_type = {'PUSH': PUSH,
             'PULL': PULL,
             'PUB': PUB,
             'SUB': SUB,
             'PAIR': PAIR}

subbed_topics = []

out_endpoints = []
in_endpoints = []


def receiver(queue, addresses, stype):
    in_sock = Socket(stype)
    
    for address in addresses:
      in_sock.bind(address)
    
    def receive_messages():
        while True:
            queue.put(in_sock.recv())
            log.info("Message received")

    receiver = threading.Thread(target=receive_messages)
    receiver.start()
    
    return in_sock

def sender(queue, addresses, stype):
    out_sock = Socket(stype)
    
    out_sock.set_int_option(SOL_SOCKET, SNDTIMEO, 1000)
    
    for address in addresses:
        endpoint = out_sock.connect(address)
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

def gate(type, queue=None, network={}, governor=None):
    if not queue:
      queue = Queue.Queue()
      
    if type == 'out':
        socket = sender(queue, network['endpoints'], stype=network['type'])
        if governor:
          governor(socket=socket, socketupdater=update, endpoints=[ep.address for ep in socket.endpoints])
    elif type == 'in':
        socket = receiver(queue, network['endpoints'], stype=network['type'])
    elif type == 'utility':
        pass
    else:
        raise ValueError("No such gate type known.")
        return Null
    
    return queue

def igate(queue=None, network={}):
  if not queue:
    queue = Queue.Queue()
    
  return gate('in', queue, network)

def ogate(queue=None, network={}):
  if not queue:
    queue = Queue.Queue()
    
  return gate('out', queue, network) 

def iogate(type, queuein=Queue.Queue(), queueout=Queue.Queue(), network={}):
    if not queue:
      queue = Queue.Queue()
      
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
        
        
def pull(queue):
    return queue.get(block=True)

def push(message, queue):
    queue.put(message)
    
    
def update(socket, operational_address):
  # Close dead endpoints
  log.debug("Updating with new addresses...")
  endpoints_tobe_removed = []
  for point in socket._endpoints:
    if point.address not in operational_address:
      endpoints_tobe_removed.append(point)
  
  log.debug('Pre:' + str(socket.endpoints))    
  for point in endpoints_tobe_removed:
      log.debug('Shutdown dead endpoint...')
      ret = nn_wrapper.nn_shutdown(socket.fd, point._endpoint_id)
      # TODO: Error checking
      socket._endpoints.remove(point)
      log.debug('Done with errno: ' + str(ret))
  log.debug('Post:' + str(socket.endpoints))
  
  # Establish new endpoints
  for point in operational_address:
    if point not in [endpoint.address for endpoint in socket.endpoints]:
      log.debug('Connecting to new endpoint address: ' + point)
      socket.connect(point)

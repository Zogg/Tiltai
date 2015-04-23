from nanomsg import Socket, PUSH, PULL, PUB, SUB, SUB_SUBSCRIBE, PAIR, SOL_SOCKET, SNDTIMEO, NanoMsgAPIError
from nanomsg import wrapper as nn_wrapper

from tiltai.utils import tiltai_logs_format

import threading
import Queue
import socket

from logbook import Logger, StderrHandler

err = StderrHandler(format_string=tiltai_logs_format)
log = Logger("network[nanolink]")


sock_type = {'PUSH': PUSH,
             'PULL': PULL,
             'PUB': PUB,
             'SUB': SUB,
             'PAIR': PAIR}

subbed_topics = []

out_endpoints = []
in_endpoints = []


def receiver(queue, addresses, stype):
    """
    Bind a queue to a listening nanomsg socket's multiple endpoints
    in a separate thread.
    
    Parameters
    ----------
    queue : Queue
        A Queue object to be filled by receiver socket
        
    addresses : list
        A list of strings of format '<protocol>://<ip>:<port>' to bind to
        
    stype : int
        One of the nanomsg scalability socket types: PUSH, PULL, PUB, SUB, PAIR
        
    Returns
    -------
        nanomsg socket object
    """
    with err.applicationbound():
      in_sock = Socket(stype)
      
      for address in addresses:
        in_sock.bind(address)
      
      def receive_messages():
          """ """
          while True:
              queue.put(in_sock.recv())
              log.info("Message received")

      receiver = threading.Thread(target=receive_messages)
      receiver.start()
      
      return in_sock

def sender(queue, addresses, stype):
    """
    Bind a queue to a connecting nanomsg socket's multiple endpoints
    in a separate thread.
    
    Parameters
    ----------
    queue : Queue
        A Queue object to be emptied by sender socket
        
    addresses : list
        A list of strings of format '<protocol>://<ip>:<port>' to bind to
        
    stype : int
        One of the nanomsg scalability socket types: PUSH, PULL, PUB, SUB, PAIR
        
    Returns
    -------
        nanomsg socket object
    """
    with err.applicationbound():
      out_sock = Socket(stype)
      
      out_sock.set_int_option(SOL_SOCKET, SNDTIMEO, 1000)
      
      for address in addresses:
          endpoint = out_sock.connect(address)
          out_endpoints.append(endpoint)
        
      def send_messages():
          """ """
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
    """
    Create, bind and manage Queue and network scalability socket interaction.
    
    This is the main method to create a self-sustained, autonomous data 
    exchange gate. Every type of networking library must provide this method.
    
    All Gates are of three types: in, out, and inout. Currently only `in` and 
    `out` are supported, with hermaphrodite type to be added soon.
    
    Parameters
    ----------
    type : string
        A type of the gate, either 'in' or 'out'
    queue : Queue
        A Queue object to be managed by socket. If None is passed, a new Queue
        is created (Default value = None)
    network : dict
        A dict of shape `{'endpoints': [], 'type': value}` is expected.
         (Default value = {})
    governor : callable
        A function to manage sockets state. More than likely it is one of the
        functions from tiltai.control.network module. If None is passed, the 
        socket state is unmanaged. (Default value = None)

    Returns
    -------
        A queue object.
    """

    with err.applicationbound():
      if not queue:
        queue = Queue.Queue()
        
      if type == 'out':
          socket = sender(queue, network['endpoints'], stype=sock_type[network['type']])
          if governor:
            governor(socket=socket, socketupdater=update, endpoints=[ep.address for ep in socket.endpoints])
      elif type == 'in':
          socket = receiver(queue, network['endpoints'], stype=sock_type[network['type']])
      else:
          raise ValueError("No such gate type known.")
          return Null
      
      return queue

def igate(queue=None, network={}):
  """

  Parameters
  ----------
  queue :
       (Default value = None)
  network :
       (Default value = {})

  Returns
  -------

  """
  if not queue:
    queue = Queue.Queue()
    
  return gate('in', queue, network)

def ogate(queue=None, network={}):
  """

  Parameters
  ----------
  queue :
       (Default value = None)
  network :
       (Default value = {})

  Returns
  -------

  """
  if not queue:
    queue = Queue.Queue()
    
  return gate('out', queue, network) 

def iogate(type, queuein=Queue.Queue(), queueout=Queue.Queue(), network={}):
    """

    Parameters
    ----------
    type :
        
    queuein :
         (Default value = Queue.Queue()

    Returns
    -------

    """
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
        """ """
        while True:
            queuein.put({'socket':in_sock, 'data': in_sock.recv()})
            log.info("Message received")
            
    def send_messages():
        """ """
        while True:
            sock.send(queueout.get(block=True))
            log.info("Message has been sent")

    receiver = threading.Thread(target=receive_messages)
    sender = threading.Thread(target=send_messages)
    receiver.start()
    sender.start()
    
    return (queuein, queueout)

  
def topic(sock, topic=None):
    """

    Parameters
    ----------
    sock :
        
    topic :
         (Default value = None)

    Returns
    -------

    """
    if topic not in subbed_topics:
        sock.set_string_option(SUB, SUB_SUBSCRIBE, topic)
        subbed_topics.append(topic)
        
        
def pull(queue):
    """

    Parameters
    ----------
    queue :
        

    Returns
    -------

    """
    return queue.get(block=True)

def push(message, queue):
    """

    Parameters
    ----------
    message :
        
    queue :
        

    Returns
    -------

    """
    queue.put(message)
    
    
def update(socket, operational_address):
  """
  Update nanomsg socket with a new list of endpoints.
  
  Parameters
  ----------
  socket : socket
      nanomsg socket object
  operational_address : list
      A list of strings of format '<protocol>://<ip>:<port>'. A list 
      represents a current state of network. Unused endpoints will be 
      disconnected, new ones will be connected to.

  """
  
  with err.applicationbound():
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

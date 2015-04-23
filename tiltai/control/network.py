import time
import threading
import socket

from logbook import Logger


log = Logger("{host} - {service}".format(host=socket.gethostname(), service="network-routine()"))

def routine(resolver, socketupdater, socket, endpoints):
  """
  Routinely update socket's endpoints with up-to-date links information.
  
  Parameters
  ----------
  resolver : callable
      A `name` -> `network address` mapper. More than likely one of resolvers
      provided by `tiltai.sdn` modules
  socketupdater : callable
      A method to update socket's endpoints
  socket : socket
      socket object, who's endpoints to manage
  endpoints : list of strings
      A list of addresses of format '<protocol>://<ip>:<port>'
  """
  
  interval = 10
  
  def update():
    """ """
    while True:
      time.sleep(interval)
      
      res_endpoints = resolver()['endpoints']
      new_list = endpoints and res_endpoints
      log.debug('New list of endpoints to be applied: ' + str(new_list))
      
      socketupdater(socket, new_list)    
      
  updater = threading.Thread(target=update)
  updater.start()

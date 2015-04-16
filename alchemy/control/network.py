import time
import threading
import socket

from logbook import Logger


log = Logger("{host} - {service}".format(host=socket.gethostname(), service="network-routine()"))

def routine(resolver, socketupdater, socket, endpoints):
  interval = 10
  
  def update():
    while True:
      time.sleep(interval)
      
      res_endpoints = resolver()['endpoints']
      new_list = endpoints and res_endpoints
      log.debug('New list of endpoints to be applied: ' + str(new_list))
      
      socketupdater(socket, new_list)    
      
  updater = threading.Thread(target=update)
  updater.start()

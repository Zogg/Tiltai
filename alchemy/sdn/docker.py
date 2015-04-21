from alchemy.network.nanolink import sock_type

import socket

from logbook import Logger


log = Logger("{host} - {service}".format(host=socket.gethostname(), service="DockerSDN"))

def dockersdn(queue_name, resolver, storage):
  """whoami"""

  hostname = socket.gethostname()
  log.debug(hostname)

  links = storage(hostname)

  if links:
    for link in links['links']:
      if link['queue'] == queue_name:
        if link.get('outgate', None):
          protocolized_nodes = ['tcp://' + address for address in resolver(link['outgate'])]
          endpoints = {'endpoints': protocolized_nodes}
        else:
          endpoints = {'endpoints': link.get('addresses', [])}
                  
        if link.get('type', None):
          endpoints['type'] = sock_type[link['type']]
        
        log.debug(endpoints)
        return endpoints

  return {'endpoints': []}

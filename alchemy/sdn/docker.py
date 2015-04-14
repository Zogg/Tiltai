import socket

from alchemy.sdn.aerospikesdn import storage
from alchemy.sdn.consulregistrator import addr
from alchemy.network.nanolink import sock_type

from logbook import Logger


log = Logger("{host} - {service}".format(host=socket.gethostname(), service="DockerSDN"))

def dockersdn(queue_name, resolver=addr, storage=storage):
  """whoami"""
  
  hostname = socket.gethostname()
  log.debug(hostname)

  links = storage(hostname)

  if links:
    for link in links['links']:
      if link['queue'] == queue_name:
        if link.get('outgate', None):
          nodes = {'nodes': resolver(link['outgate'])}
        else:
          nodes = {'ports': link.get('ports', [])}
                  
        if link.get('type', None):
          nodes['type'] = sock_type[link['type']]
        
        log.debug(nodes)
        return nodes

  return {'nodes': []}

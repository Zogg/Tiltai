import socket

from sdn.aerospike import storage

def dockersdn(queue_name, resolver=None, storage=None):
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

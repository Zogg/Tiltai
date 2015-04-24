from tiltai.utils import tiltai_logs_format

import socket

from logbook import Logger, StderrHandler


err = StderrHandler(format_string=tiltai_logs_format)
log = Logger("sdn[docker]")

def dockersdn(queue_name, resolver, storage):
  """
  Get addresses and type of the socket from within docker container. A 
  hostname of the container is used as the identifier to receive network links
  definition.

  Parameters
  ----------
  queue_name : string
      Name of the queue, for which to get network settings
  resolver : callable
      A `name` -> `network address` mapper. More than likely one of resolvers
      provided by `tiltai.sdn` modules
  storage : callable
      A data backend which provides network mapping: definition of links 
      between gates. More than likely one of the methods provided by 
      `tiltai.sdn` modules

  Returns
  -------
  network : dict
      A dict of shape `{'endpoints': [], 'type': value}`
  """
  
  with err.applicationbound():
    hostname = socket.gethostname()
    log.debug('My hostname is: ' + hostname)

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
            endpoints['type'] = link['type']
          
          log.debug('Topology resolved to ip addresses: ' + str(endpoints))
          return endpoints

    return {'endpoints': []}

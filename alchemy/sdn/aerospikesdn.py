import aerospike
import socket

from logbook import Logger


log = Logger("{host} - {service}".format(host=socket.gethostname(), service="aerospikesdn"))

config = {
  'hosts': [
      ( '172.17.42.1', 3000 )
  ],
  'policies': {
      'timeout': 1000 # milliseconds
  }
}


def storage(hostname):
  client = aerospike.client(config)
  client.connect()

  key = ('sdn', 'service', hostname)
  (key, meta, links) = client.select(key, ['links'])
  client.close()
  return links
  
  
def upload_links(data):
  client = aerospike.client(config)
  client.connect()
  
  for service, links in data.iteritems():
    client.put(('sdn','service',service), links)
  
  for service, links in data.iteritems():
    (key, meta, links) = client.select(('sdn','service',service), ['links'])
    log.info(links)  
    
  client.close()

  
  

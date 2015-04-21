import json
import socket

from logbook import Logger


log = Logger("{host} - {service}".format(host=socket.gethostname(), service="Consul-Registrator address"))


def get_topology(servicename):
  with file('linksdb.json', 'r') as dbfile:
    return json.load(dbfile)[servicename]
  
  
def put_topology(topology):
  with file('linksdb.json', 'w') as db:
    json.dump(topology, db)

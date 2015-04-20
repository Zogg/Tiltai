import json
import socket

from logbook import Logger


log = Logger("{host} - {service}".format(host=socket.gethostname(), service="Consul-Registrator address"))


def storage(hostname):
  with file('linksdb.json', 'r') as dbfile:
    return json.load(dbfile)[hostname]
  
  
def upload_links(data):
  with file('linksdb.json', 'w') as db:
    json.dump(data, db)

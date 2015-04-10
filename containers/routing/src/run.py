from control import gate, iogate, push, pull
from nanomsg import PUSH, PULL, PUB, SUB, REQ, REP

from consullib import addr

import time
import hashlib
import json

devopsdb = {'encryptor': [{'queue': 'statusreport', 'outgate': 'emailsink'}],
            'linksdb': [{'queue': 'ioqueue', 'ports': [5678]}]}

def mesossdn():
  """whoami"""
  return {'nodes': addr()}


def dockersdn(queue_name):
  """whoami"""
  import socket
  hostname = socket.gethostname()

  links = devopsdb.get(hostname)
  if links:
    for link in links:
      if link['queue'] == queue_name:
        return {'nodes': addr(link['outgate'])}

  return {'nodes': []}

def linksdb():
    iqueue, oqueue = iogate('in', network={'ports': [5678], 'type': REP})

    while True:
        packet = pull(iqueue)
        query = json.loads(packet['data'])
        service = devopsdb.get(query['service'])
        
        if service:
          packet['data'] = json.dumps(service)
          
        push(packet, oqueue)


if __name__ == '__main__':
  linksdb()

from kazoo.client import KazooClient

import json

config = {'hosts': '127.0.0.1:2181'}


def addr(service, blocking=True): 
  pass

def get_topology(servicename, config=config):
  zk = KazooClient(**config)
  zk.start()
  
  try:
    topology, stat = zk.get("/sdn/services/{name}".format(name=servicename))
  except Exception as e:
    #TODO
    pass
    
  zk.stop()
  
  topology = json.loads(topology)
  return topology
  
def put_topology(topology, config=config):
  zk = KazooClient(**config)
  zk.start()
  
  for service, links in topology.iteritems():
    if zk.exists("/sdn/services/{name}".format(name=service)):
      zk.set("/sdn/services/{name}".format(name=service), json.dumps(links))
    else:
      zk.ensure_path("/sdn/services")
      zk.create("/sdn/services/{name}".format(name=service), json.dumps(links))
      
  ret_check = zk.get_children("/sdn/services")
  zk.stop()
  
  return ret_check

import dns.resolver
import consulate
import time
import socket

from logbook import Logger


log = Logger("{host} - {service}".format(host=socket.gethostname(), service="Consul-Registrator address"))

def addr(service, blocking=True):
  answered = False
  
  while not answered:
    try:
      r = dns.resolver.query(service, 'SRV', tcp=True)
    except Exception as e:
      log.warn('Could not find address of the service: {0}'.format(service))
      log.warn(str(e))
      if blocking:
        time.sleep(10)
        log.warn("Retrying...")
        continue
      else:
        return []

    port_fqdn = [(srvrecord.port, srvrecord.target.to_text()) for srvrecord in r]
    fqdn_ip = dict([(record.to_text().split()[0], record.to_text().split()[4]) for record in r.response.additional])

    addresses = []

    for srvrecord in port_fqdn:
      addresses.append(fqdn_ip[srvrecord[1]] + ':' + str(srvrecord[0]))

    log.debug(r.response)
    log.debug(addresses)
    return addresses


def get_topology(servicename, blocking=True):
  answered = False
  
  while not answered:
    try:
      session = consulate.Session()
    except Exception as e:
      log.warn(str(e))
      if blocking:
        time.sleep(10)
        log.warn("Retrying...")
        continue
      else:
        return []

    try:
      return session.kv['sdn-services-{name}'.format(name=servicename)]['links']
    except KeyError as e:
      log.error(e)
      return {}


def put_topology(topology, blocking=True):
  session = consulate.Session()

  for service, links in topology.iteritems():
    session.kv['sdn-services-{name}'.format(name=service)] = links

  return [key for key in session.kv.find('sdn-services')]  
import dns.resolver
import consulate
import time
import socket

from tiltai.utils import tiltai_logs_format

from logbook import Logger, StderrHandler


err = StderrHandler(format_string=tiltai_logs_format)
log = Logger("sdn[consulregistrator]")

def addr(service, blocking=True):
  """
  Query Consul's DNS interface.
  
  Parameters
  ----------
  service : string
      Name of the service
  blocking : bool
      Query for the service until it is discovered (Default value = True)

  Returns
  -------
      list
      List of strings in shape of `<ip>:<port>`
  """
  
  with err.applicationbound():
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
  """
  Retrieve network topology from Consul's key/value store.
  
  Parameters
  ----------
  servicename :
      Name of the service
  blocking :
      Retry if session to the Consul server may not be established
       (Default value = True)

  Returns
  -------
      list of dicts
      List of dicts in shape of, example:
          `[{"outgate": "emailsink", "queue": "encrypted", "type": "PUSH"},
            {"addresses": ["tcp://0.0.0.0:4567"], "queue": "plaintext", 
                                                  "type": "PULL"}]`
  """

  with err.applicationbound():
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
  """
  Store network topology to Consul's key/value store.
  
  Parameters
  ----------
  topology : dict
      Topology definition
  blocking :
      Retry if session to the Consul server may not be established
       (Default value = True)

  Returns
  -------

  """

  with err.applicationbound():
    session = consulate.Session()

    for service, links in topology.iteritems():
      session.kv['sdn-services-{name}'.format(name=service)] = links

    return [key for key in session.kv.find('sdn-services')]  

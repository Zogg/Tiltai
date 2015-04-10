import dns.resolver
import time

def addr(service, blocking=True):
  answered = False
  
  while not answered:
    try:
      r = dns.resolver.query(service, 'SRV')
    except Exception as e:
      print('Could not find address', service, e)
      if blocking:
        time.sleep(10)
        print("Retrying...")
        continue
      else:
        return []

    port_fqdn = [(srvrecord.port, srvrecord.target.to_text()) for srvrecord in r]
    fqdn_ip = dict([(record.to_text().split()[0], record.to_text().split()[4]) for record in r.response.additional])

    addresses = []

    for srvrecord in port_fqdn:
      addresses.append({'port':srvrecord[0], 'ip':fqdn_ip[srvrecord[1]]})

    print(r.response)
    return addresses

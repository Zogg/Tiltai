import aerospike

config = {
  'hosts': [
      ( '172.17.42.1', 3000 )
  ],
  'policies': {
      'timeout': 1000 # milliseconds
  }
}

client = aerospike.client(config)

def storage(hostname):
  client.connect()

  key = ('sdn', 'service', hostname)
  (key, meta, links) = client.select(key, ['links'])
  return links

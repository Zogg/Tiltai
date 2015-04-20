So how did we end in that state? Lets start from beginning. The main problem here is that we have to know the addresses of the service to which we want to connect in advance. In case of scalable application, that will be many, many addresses.

We could pass the address for the socket to connect to in the sourcecode - a hardcoded address. We could put it somewhere in the configuration file, but that would not make it less hardcoded than that. That is doable, and gate() would work as expected with this code:

.. highlight:: python

  plaintext = gate('out', network={'endpoints': ['tcp://127.0.0.1:5555'], 
                                   'type': 'PUSH'}) 


We want to get rid of the static addresses and leave it up to the devops to link the services. Hence, the next step is to figure out where do we export the static data to. For the sake of example, I'v chosen progrium/consul and /registrator as service discovery service. Every time a new docker containers popups in the host, /registrator registers it in the consul. We may then query consul's dns interface and get addresses of the desired services::

  from alchemy.sdn.consulregistrator import addr

  plaintext = gate('out', network={'endpoints': addr('encryptor'), 
                                   'type': 'PUSH'}) 


So now we query consul by docker container's name and get all the addresses of all the 'encryptors' that would be running. However, the type of the socket to use still remains hardcoded. As the ports and IP assignments are taken care by DCOS, 


  from alchemy.sdn.consulregistrator import addr

  plaintext = gate('out', network=dockersdn('plaintext', )) 





  from alchemy.sdn.consulregistrator import addr

  plaintext = gate('out', network=dockersdn('plaintext'),
                          governor=partial(routine, resolver=partial(dockersdn, 'plaintext')))) 




  def ogate(queue_name):
    return gate('out', network=dockersdn(queue_name),
                       governor=partial(routine, resolver=partial(dockersdn, queue_name)))) 

  plaintext = ogate('plaintext')





from machines import TaChiKoma
                     
machine = TaChiKoma(gate, dockersdn, routine)

plaintext = machine.ogate('plaintext')


.. Alchemy documentation master file, created by
   sphinx-quickstart on Fri Apr 17 11:21:49 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Tiltai's documentation!
===================================

Tiltas is a collection of parts to bring development of microservices (and services) up to XXI century capabilities. By providing a concept of **gate**: an autonomous network interface with built-in capabilities of state control, service discovery and separation of cencerns. 

It does so by conveniently wrapping common network scalability protocols and popular service discovery methods, and much much more. This way, a developer may assemble powerful machine tailored for her's own DCOS/PaaS environment, the same way one could assemble a particular automobile from spare but compatible parts::

  from alchemy.network.nanolink import gate, push, pull
  from alchemy.sdn.docker import dockersdn
  from alchemy.control.network import routine

  from functools import partial

  def feeder():
    plaintext = gate('out', network=dockersdn('plaintext'), 
                            governor=partial(routine, resolver=partial(dockersdn, 'plaintext')))

    while True:
        push("Plaintext message", plaintext)
        time.sleep(3)


The service defined above is run on Apache Mesos with Marathon, packed in a Docker container. The gate returns a Queue, everything that is put in the queue is delivered to a services, which at the time of service development, are yet unknown. The links between services are defined externally (i.e. by devops), and are retrieved during runtime. 


Why Tiltai
==========

Contents:

.. toctree::
   :maxdepth: 2


API Docs
        
.. automodule:: alchemy.network.nanolink
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


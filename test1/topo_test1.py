#!/usr/bin/python

from mininet.topo import Topo

'''

File name: flowvisor_test1.py

         H1
           \
            \
             S1 ----------- S2 ----- H3
            /
           /
         H2
			
For running type:
sudo mn --custom topo_test1.py --topo topo_test1 --link tc --controller remote --mac --arp
			
'''

class topoTest1(Topo):
	def __init__(self):
	
		# Initialize topology
		Topo.__init__(self)
	
		# Create template host, switch, and link
		hconfig = {'inNamespace':True}
		link_config = {'bw': 100}
		host_link_config = {}
	
		# Create switch nodes			
		self.addSwitch('s1')		
		self.addSwitch('s2')
	
		# Create host nodes
		self.addHost('h1',**hconfig)
		self.addHost('h2',**hconfig)
		self.addHost('h3',**hconfig)
	
		# Add switch links
		self.addLink('s1', 's2', **link_config)
	
		# Add host links
		self.addLink('h1', 's1', **link_config)
		self.addLink('h2', 's1', **link_config)
		self.addLink('h3', 's2', **link_config)	

topos = { 'topo_test1': ( lambda: topoTest1() ) }


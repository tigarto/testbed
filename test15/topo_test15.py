#!/usr/bin/python

from mininet.topo import Topo

'''
File name: topo_test15.py

         H1
           \
            \
             S1 ----- H3
            /
           /
         H2
			
For running type:
sudo mn --custom topo_test15.py --topo topo_test15 --link tc --controller remote --mac --arp
			
'''

class topoTest15(Topo):
	def __init__(self):
	
		# Initialize topology
		Topo.__init__(self)
	
		# Create template host, switch, and link
		hconfig = {'inNamespace':True}
		link_config = {'bw': 100}
		host_link_config = {}
	
		# Create switch nodes			
		self.addSwitch('s1')		
			
		# Create host nodes
		self.addHost('h1',**hconfig)
		self.addHost('h2',**hconfig)
		self.addHost('h3',**hconfig)
	
		
		# Add host links
		self.addLink('h1', 's1', **link_config)
		self.addLink('h2', 's1', **link_config)
		self.addLink('h3', 's1', **link_config)	

topos = { 'topo_test15': ( lambda: topoTest15() ) }

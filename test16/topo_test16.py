#!/usr/bin/python

from mininet.topo import Topo

'''
File name: topo_test16.py

         H1                     H3
           \                   /   
            \                 /
             S1 ----------- S2 
            /                 \
           /                   \
         H2                     H4
			
For running type:
sudo mn --custom topo_test16.py --topo topo_test16 --link tc --controller remote --mac --arp
			
'''

class topoTest16(Topo):
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
		h1 = self.addHost('h1',**hconfig)
		h2 = self.addHost('h2',**hconfig)
		h3 = self.addHost('h3',**hconfig)
		h4 = self.addHost('h4',**hconfig)
	
		# Links
		# s1 <---> h1, h2
		self.addLink('h1','s1', **link_config)
		self.addLink('h2','s1', **link_config)
		
		# s1 <---> s2
		self.addLink('s1','s2',**link_config)
	
			
		# s2 <---> h3, h4
		self.addLink('h3','s2', **link_config)
		self.addLink('h4','s2', **link_config)	

topos = { 'topo_test16': ( lambda: topoTest16() ) }


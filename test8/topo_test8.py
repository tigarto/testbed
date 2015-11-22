#!/usr/bin/python

from mininet.topo import Topo

'''

File name: flowvisor_test1.py

         H1                     HTTP
           \                   /   
            \                 /
             S1 ----------- S2 
            /                 \
           /                   \
         H2                     FTP
			
For running type:
sudo mn --custom topo_test8.py --topo topo_test8 --link tc --controller remote --mac --arp
			
'''

class topoTest8(Topo):
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
		http = self.addHost('http',**hconfig)
		ftp = self.addHost('ftp',**hconfig)
	
		# Add switch links
		self.addLink('s1','s2',**link_config)
	
		# Add host links
		self.addLink('h1','s1', **link_config)
		self.addLink('h2','s1', **link_config)
		self.addLink('http','s2',**link_config)
		self.addLink('ftp','s2',**link_config)	

topos = { 'topo_test8': ( lambda: topoTest8() ) }


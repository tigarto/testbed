#!/usr/bin/python

from mininet.topo import Topo

'''

File name: flowvisor_test5.py


             H1
              |
         H2   |                 http
           \  |                / 
            \ |               /
             S1 ----------- S2
            / |               \ 
           /  |                \
         H3   |                 ftp
              |
             H4
			
For running type:
sudo mn --custom topo_test6.py --topo topo_test6 --controller remote --mac --arp
			
'''

class topoTest6( Topo ):
	"Simple topology example."
	def __init__( self ):
		"Create custom topo."
		# Initialize topology
		Topo.__init__( self )
		
		hconfig = {'inNamespace':True}

		
		# Add hosts and switches
		http = self.addHost( 'http' , **hconfig)
		ftp = self.addHost( 'ftp' , **hconfig)
		h1 = self.addHost( 'h1' , **hconfig)
		h2 = self.addHost( 'h2' , **hconfig)
		h3 = self.addHost( 'h3' , **hconfig)
		h4 = self.addHost( 'h4' , **hconfig)
		s1 = self.addSwitch( 's1' )
		s2 = self.addSwitch( 's2' )
		
		# Add links
		self.addLink( h1, s1 )
		self.addLink( h2, s1 )
		self.addLink( h3, s1 )
		self.addLink( h4, s1 )
		self.addLink( s2, http )
		self.addLink( s2, ftp )
		self.addLink( s1, s2 )
		
topos = { 'topo_test6': ( lambda: topoTest6() ) }

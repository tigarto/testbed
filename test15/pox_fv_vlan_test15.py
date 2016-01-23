from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr

log = core.getLogger()

s1_dpid=0


# Se metieron aca las colas

def _handle_ConnectionUp(event):
	global s1_dpid
	print "ConnectionUp: ", dpidToStr(event.connection.dpid)
	#remember the connection dpid for switch 
	for m in event.connection.features.ports:
		if m.name == "s1-eth1":
			s1_dpid = event.connection.dpid
			print "s1_dpid = ", s1_dpid

def _handle_PacketIn(event):
	global s1_dpid
	# print "PacketIn: ", dpidToStr(event.connection.dpid)

	if event.connection.dpid==s1_dpid:
	   # Flujo entrante por el puerto 3 con dl_vlan = 50 
		msg = of.ofp_flow_mod()
		msg.priority = 100				# A numero mas alto mayor prioridad 
		msg.idle_timeout = 0
		msg.hard_timeout = 0
		msg.match.in_port = 3
		msg.match.dl_vlan = 50
		msg.actions.append(of.ofp_action_output(port = 1))
		event.connection.send(msg)
				
		# Flujo entrante por el puerto 3 con dl_vlan = 60 
		msg = of.ofp_flow_mod()		
		msg.priority = 1
		msg.idle_timeout = 0
		msg.hard_timeout = 0
		msg.match.in_port = 3
		msg.match.dl_vlan = 60
		msg.actions.append(of.ofp_action_output(port = 2))
		event.connection.send(msg)
		
		# Flujo entrante por el puerto 1
		msg = of.ofp_flow_mod()		
		msg.priority = 1
		msg.idle_timeout = 0
		msg.hard_timeout = 0
		msg.match.in_port = 1		
		msg.actions.append([of.ofp_action_vlan_vid(vlan_vid = 50),of.ofp_action_output(port = 3)])
		event.connection.send(msg)
		
		# Flujo entrante por el puerto 2
		msg = of.ofp_flow_mod()		
		msg.priority = 1
		msg.idle_timeout = 0
		msg.hard_timeout = 0
		msg.match.in_port = 2		
		msg.actions.append([of.ofp_action_vlan_vid(vlan_vid = 60),of.ofp_action_output(port = 1)])
		event.connection.send(msg)

	
def launch ():
	core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
	core.openflow.addListenerByName("PacketIn", _handle_PacketIn) 

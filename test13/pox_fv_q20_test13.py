from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr

log = core.getLogger()

s1_dpid=0
s2_dpid=0

# Se metieron aca las colas

def _handle_ConnectionUp(event):
	global s1_dpid, s2_dpid
	print "ConnectionUp: ", dpidToStr(event.connection.dpid)

	#remember the connection dpid for switch 
	for m in event.connection.features.ports:
		if m.name == "s1-eth1":
			s1_dpid = event.connection.dpid
			print "s1_dpid = ", s1_dpid
		elif m.name == "s2-eth1":
			s2_dpid = event.connection.dpid
			print "s2_dpid = ", s2_dpid


def _handle_PacketIn(event):
	global s1_dpid, s2_dpid
	# print "PacketIn: ", dpidToStr(event.connection.dpid)

	if event.connection.dpid==s1_dpid:
	   # Flujo entrante por el puerto 2 (h1 --- s1)
		msg = of.ofp_flow_mod()
		msg.priority = 100				# A numero mas alto mayor prioridad 
		msg.idle_timeout = 0
		msg.hard_timeout = 0
		msg.match.in_port = 2	
		msg.match.dl_type = 0x0800
		msg.match.nw_proto = 6
		msg.match.tp_src=4000			
		msg.actions.append(of.ofp_action_enqueue(port = 1, queue_id = 1))
		event.connection.send(msg)
				
		# Flujo entrante por el puerto 1 (s1 --- s2)
		msg = of.ofp_flow_mod()
		msg.priority = 1
		msg.idle_timeout = 0
		msg.hard_timeout = 0
		msg.match.in_port = 1
		msg.match.dl_type = 0x0800
		msg.match.nw_proto = 6
		msg.match.tp_dst=4000 	# Aqui tengo mis dudas por ser dos switches?	
		msg.actions.append(of.ofp_action_output(port = 2))
		event.connection.send(msg)

	if event.connection.dpid==s2_dpid:			
		
		# Flujo entrante por el puerto 2 (s2 --- h2)
		msg = of.ofp_flow_mod()
		msg.priority = 100				# A numero mas alto mayor prioridad 
		msg.idle_timeout = 0
		msg.hard_timeout = 0
		msg.match.in_port = 2
		msg.match.dl_type = 0x0800
		msg.match.nw_proto = 6
		msg.match.tp_dst=4000
		msg.actions.append(of.ofp_action_enqueue(port = 1, queue_id = 1))
		event.connection.send(msg)
		
		# Flujo entrante por el puerto 1 (s1 --- s2)
		msg = of.ofp_flow_mod()
		msg.priority = 1
		msg.idle_timeout = 0
		msg.hard_timeout = 0
		msg.match.in_port = 1
		msg.match.dl_type = 0x0800
		msg.match.nw_proto = 6
		msg.match.tp_src=4000 	# Aqui tengo mis dudas por ser dos switches?		
		msg.actions.append(of.ofp_action_output(port = 2))
		event.connection.send(msg)
		
def launch ():
	core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
	core.openflow.addListenerByName("PacketIn", _handle_PacketIn) 


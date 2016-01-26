from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr
from pox.lib.addresses import EthAddr

log = core.getLogger()

s1_dpid=0
s2_dpid=0

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
	
	# switch s1
	if event.connection.dpid==s1_dpid:

	   # Flujos para la tabla de flujos del switch
		flow_s1_0 = of.ofp_flow_mod()
		flow_s1_0.priority = 32768 # A mayor valor mas prioridad
		flow_s1_0.match.in_port = 1
		flow_s1_0vlan_id = of.ofp_action_vlan_vid(vlan_vid = 10)
		flow_s1_queue1 = of.ofp_action_enqueue(port = 3, queue_id = 1))
		flow_s1_0.actions = [flow_s1_0vlan_id,flow_s1_queue1]
		
		flow_s1_1 = of.ofp_flow_mod()
		flow_s1_1.priority = 32768 # A mayor valor mas prioridad
		flow_s1_1.match.in_port = 2
		flow_s1_1vlan_id = of.ofp_action_vlan_vid(vlan_vid = 20)
		flow_s1_queue2 = of.ofp_action_enqueue(port = 3, queue_id = 2))
		flow_s1_1.actions = [flow_s1_1vlan_id,flow_s1_queue2]


	   	flow_s1_2 = of.ofp_flow_mod()
		flow_s1_2.priority = 32768 # A mayor valor mas prioridad
		flow_s1_2.match.dl_vlan = 10
		flow_s1_2stripvlan = of.ofp_action_strip_vlan()
		flow_s1_2out = of.ofp_action_output(port = 1)
		flow_s1_2.actions = [flow_s1_2stripvlan,flow_s1_2out]
			   
	   	flow_s1_3 = of.ofp_flow_mod()
		flow_s1_3.priority = 32768 # A mayor valor mas prioridad
		flow_s1_3.match.dl_vlan = 20
		flow_s1_3stripvlan = of.ofp_action_strip_vlan()
		flow_s1_3out = of.ofp_action_output(port = 2)
		flow_s1_3.actions = [flow_s1_3stripvlan,flow_s1_3out]
		
		# Instalacion de los flujos previamente definidos
		core.openflow.sendToDPID(s1_dpid,flow_s1_0)
		core.openflow.sendToDPID(s1_dpid,flow_s1_1)
		core.openflow.sendToDPID(s1_dpid,flow_s1_2)
		core.openflow.sendToDPID(s1_dpid,flow_s1_3)
	
	# switch s2
	if event.connection.dpid==s2_dpid:			
		
		# Flujos para la tabla de flujos del switch
		flow_s2_0 = of.ofp_flow_mod()
		flow_s2_0.priority = 32768 # A mayor valor mas prioridad
		flow_s2_0.match.in_port = 2
		flow_s2_0vlan_id = of.ofp_action_vlan_vid(vlan_vid = 20)
		flow_s2_queue2 = of.ofp_action_enqueue(port = 1, queue_id = 2))
		flow_s2_0.actions = [flow_s2_0vlan_id,flow_s2_queue2]
		
		flow_s2_1 = of.ofp_flow_mod()
		flow_s2_1.priority = 32768 # A mayor valor mas prioridad
		flow_s2_1.match.in_port = 3
		flow_s2_1vlan_id = of.ofp_action_vlan_vid(vlan_vid = 10)
		flow_s2_queue1 = of.ofp_action_enqueue(port = 1, queue_id = 1))
		flow_s2_1.actions = [flow_s2_1vlan_id,flow_s2_queue1]

	   	flow_s2_2 = of.ofp_flow_mod()
		flow_s2_2.priority = 32768 # A mayor valor mas prioridad
		flow_s2_2.match.dl_vlan = 10
		flow_s2_2stripvlan = of.ofp_action_strip_vlan()
		flow_s2_2out = of.ofp_action_output(port = 3)
		flow_s2_2.actions = [flow_s2_2stripvlan,flow_s2_2out]
			   
	   	flow_s2_3 = of.ofp_flow_mod()
		flow_s2_3.priority = 32768 # A mayor valor mas prioridad
		flow_s2_3.match.dl_vlan = 20
		flow_s2_3stripvlan = of.ofp_action_strip_vlan()
		flow_s2_3out = of.ofp_action_output(port = 2)
		flow_s2_3.actions = [flow_s2_3stripvlan,flow_s2_3out]	
		
		# Instalacion de los flujos previamente definidos
		core.openflow.sendToDPID(s2_dpid,flow_s2_0)
		core.openflow.sendToDPID(s2_dpid,flow_s2_1)
		core.openflow.sendToDPID(s2_dpid,flow_s2_2)
		core.openflow.sendToDPID(s2_dpid,flow_s2_3)
		
def launch ():
	core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
	core.openflow.addListenerByName("PacketIn", _handle_PacketIn) 
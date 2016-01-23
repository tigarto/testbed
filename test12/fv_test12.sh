#!/bin/sh
#sudo /etc/init.d/flowvisor restart  // Solo para la primera vez que se corra
fvctl -f /dev/null set-config --enable-topo-ctrl  
fvctl -f /dev/null remove-slice VN1
fvctl -f /dev/null remove-slice VN2


# Agregando las slices (Redes virtuales)
fvctl -f /dev/null add-slice VN1 tcp:localhost:10001 araif@udea.edu.co
fvctl -f /dev/null add-slice VN2 tcp:localhost:10002 araif@udea.edu.co


# Agregando los flowspaces de cada slice

# ---- Slice 1 (VN1) ---- #



# Switch: S1
fvctl -f /dev/null add-flowspace -q 1 VN1_flow1 1 100 in_port=1,tp_src=4000 VN1=7
fvctl -f /dev/null add-flowspace -q 1 VN1_flow2 1 100 in_port=1,tp_dst=4000 VN1=7
fvctl -f /dev/null add-flowspace VN1_flow3 1 100 in_port=2 VN1=7
# Switch: S2
fvctl -f /dev/null add-flowspace -q 1 VN1_flow4 2 100 in_port=1,tp_src=4000 VN1=7
fvctl -f /dev/null add-flowspace -q 1 VN1_flow5 2 100 in_port=1,tp_dst=4000 VN1=7
fvctl -f /dev/null add-flowspace VN1_flow6 2 100 in_port=2 VN1=7

# ---- Slice 2 (VN2) ---- #


# Switch: S1
fvctl -f /dev/null add-flowspace -q 2 VN2_flow1 1 10 in_port=1,tp_src=5000 VN2=7
fvctl -f /dev/null add-flowspace -q 2 VN2_flow2 1 10 in_port=1,tp_dst=5000 VN2=7
fvctl -f /dev/null add-flowspace VN2_flow3 1 10 in_port=2 VN2=7
# Switch: S2
fvctl -f /dev/null add-flowspace -q 2 VN2_flow4 2 10 in_port=1,tp_src=5000 VN2=7
fvctl -f /dev/null add-flowspace -q 2 VN2_flow5 2 10 in_port=1,tp_dst=5000 VN2=7
fvctl -f /dev/null add-flowspace VN2_flow6 2 10 in_port=2 VN2=7


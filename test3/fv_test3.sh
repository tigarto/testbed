#!/bin/sh
#sudo /etc/init.d/flowvisor restart  // Solo para la primera vez que se corra
fvctl -f /dev/null remove-slice VN1
fvctl -f /dev/null remove-slice VN2

# Agregando las slices (Redes virtuales)
fvctl -f /dev/null add-slice VN2 tcp:localhost:10002 araif@udea.edu.co

# Agregando los flowspaces de cada slice

# Slice 2 (VN2)
fvctl -f /dev/null add-flowspace VN2_flow1 1 1 in_port=3 VN2=7
fvctl -f /dev/null add-flowspace VN2_flow2 1 1 in_port=1 VN2=7
fvctl -f /dev/null add-flowspace VN2_flow3 2 1 any VN2=7


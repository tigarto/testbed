#!/bin/sh
#sudo /etc/init.d/flowvisor restart  // Solo para la primera vez que se corra
fvctl -f /dev/null remove-slice VN1


# Agregando las slices (Redes virtuales)
fvctl -f /dev/null add-slice VN1 tcp:localhost:10001 araif@udea.edu.co

# Agregando los flowspaces de cada slice

# Slice 1 (VN1)
fvctl -f /dev/null add-flowspace VN1_flow1 1 1 in_port=2 VN1=7
fvctl -f /dev/null add-flowspace VN1_flow2 1 1 in_port=1 VN1=7
fvctl -f /dev/null add-flowspace VN1_flow3 2 1 any VN1=7



#!/bin/sh
#sudo /etc/init.d/flowvisor restart  // Solo para la primera vez que se corra
fvctl -f /dev/null remove-slice VN1
#fvctl -f /dev/null remove-slice VN2


# Agregando las slices (Redes virtuales)
fvctl -f /dev/null add-slice VN1 tcp:localhost:10001 araif@udea.edu.co
#fvctl -f /dev/null add-slice VN2 tcp:localhost:10002 araif@udea.edu.co

# Agregando los flowspaces de cada slice

# Slice 1 (VN1)
fvctl -f /dev/null add-flowspace VN1_flow1 1 1 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:03 VN1=7
fvctl -f /dev/null add-flowspace VN1_flow2 1 1 dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:01 VN1=7
fvctl -f /dev/null add-flowspace VN1_flow3 2 1 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:03 VN1=7
fvctl -f /dev/null add-flowspace VN1_flow4 2 1 dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:01 VN1=7

# Slice 2 (VN2)
#fvctl -f /dev/null add-flowspace VN2_flow1 1 1 dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:03 VN2=7
#fvctl -f /dev/null add-flowspace VN2_flow2 1 1 dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:02 VN2=7
#fvctl -f /dev/null add-flowspace VN2_flow3 2 1 dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:03 VN2=7
#fvctl -f /dev/null add-flowspace VN2_flow4 2 1 dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:02 VN2=7



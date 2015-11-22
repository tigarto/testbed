#!/bin/sh
#sudo /etc/init.d/flowvisor restart  // Solo para la primera vez que se corra

fvctl -f /dev/null remove-slice HTTP
fvctl -f /dev/null remove-slice FTP

# Agregando las slices (Redes virtuales)

fvctl -f /dev/null add-slice HTTP tcp:localhost:10001 araif@udea.edu.co
fvctl -f /dev/null add-slice FTP tcp:localhost:10002 araif@udea.edu.co
fvctl -f /dev/null set-config --enable-topo-ctrl  

# Agregando los flowspaces de cada slice

# ==== Slice (http) ====

# switch s1

fvctl -f /dev/null add-flowspace http_ARP_F1 any 110 dl_type=0x806,nw_src=10.0.0.2,dl_src=00:00:00:00:00:02 HTTP=7
fvctl -f /dev/null add-flowspace http_ARP_F2 any 110 dl_type=0x806,nw_src=10.0.0.4,dl_src=00:00:00:00:00:04 HTTP=7

fvctl -f /dev/null add-flowspace http_F1 1 100 in_port=2 HTTP=7
fvctl -f /dev/null add-flowspace -f 1 http_F2 1 100 in_port=1,tp_src=8000 HTTP=7
fvctl -f /dev/null add-flowspace -f 1 http_F3 1 100 in_port=1,tp_dst=8000 HTTP=7


# switch s2
fvctl -f /dev/null add-flowspace -f 1 http_F4 2 100 in_port=1,tp_src=8000 HTTP=7
fvctl -f /dev/null add-flowspace -f 1 http_F5 2 100 in_port=1,tp_dst=8000 HTTP=7
fvctl -f /dev/null add-flowspace http_F6 2 100 in_port=2 HTTP=7

# ==== Slice (ftp) ====

# switch s1
fvctl -f /dev/null add-flowspace ftp_F1 1 10 in_port=3 FTP=7
fvctl -f /dev/null add-flowspace -f 2 ftp_F2 1 10 in_port=1 FTP=7


# switch s2
fvctl -f /dev/null add-flowspace -f 2 ftp_F3 2 10 in_port=1 FTP=7
fvctl -f /dev/null add-flowspace ftp_F4 2 10 in_port=3 FTP=7

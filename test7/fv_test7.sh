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

fvctl  -f /dev/null add-flowspace http_ARP_F1 any 110 dl_type=0x806,nw_src=10.0.0.2,dl_src=00:00:00:00:00:02 HTTP=7
fvctl  -f /dev/null add-flowspace http_ARP_F2 any 110 dl_type=0x806,nw_src=10.0.0.3,dl_src=00:00:00:00:00:03 HTTP=7
fvctl  -f /dev/null add-flowspace http_ARP_F3 any 110 dl_type=0x806,nw_src=10.0.0.6,dl_src=00:00:00:00:00:06 HTTP=7
#fvctl  -f /dev/null add-flowspace http_ARP_F4 any 110 dl_type=0x806,nw_src=10.0.0.6,nw_dst=10.0.0.2 HTTP=7
#fvctl  -f /dev/null add-flowspace http_ARP_F1 any 110 dl_type=0x806,dl_src=00:00:00:00:00:01,nw_src=10.0.0.1,nw_dst=10.0.0.6 HTTP=7
#fvctl  -f /dev/null add-flowspace http_ARP_F2 any 110 dl_type=0x806,dl_src=00:00:00:00:00:02,nw_src=10.0.0.2,nw_dst=10.0.0.6 HTTP=7    
#fvctl  -f /dev/null add-flowspace http_ARP_F3 any 110 dl_type=0x806,dl_src=00:00:00:00:00:06,nw_dst=10.0.0.1 HTTP=7
#fvctl  -f /dev/null add-flowspace http_ARP_F4 any 110 dl_type=0x806,dl_src=00:00:00:00:00:06,nw_dst=10.0.0.2 HTTP=7    

fvctl -f /dev/null add-flowspace http_F1 1 100 in_port=1 HTTP=7
fvctl -f /dev/null add-flowspace http_F2 1 100 in_port=2 HTTP=7
fvctl -f /dev/null add-flowspace http_F3 1 100 in_port=5,tp_src=8000 HTTP=7
fvctl -f /dev/null add-flowspace http_F4 1 100 in_port=5,tp_dst=8000 HTTP=7
#fvctl -f /dev/null add-flowspace http_F3 1 100 in_port=5,dl_type=0x0800,nw_proto=6,nw_src=10.0.0.6,dl_src=00:00:00:00:00:06 HTTP=7
#fvctl -f /dev/null add-flowspace http_F4 1 100 in_port=5,dl_type=0x0800,nw_proto=6,nw_dst=10.0.0.6,dl_dst=00:00:00:00:00:06 HTTP=7
#fvctl -f /dev/null add-flowspace http_F3 1 100 in_port=5,dl_type=0x0800,nw_proto=6,tp_src=8000 HTTP=7
#fvctl -f /dev/null add-flowspace http_F4 1 100 in_port=5,dl_type=0x0800,nw_proto=6,tp_dst=8000 HTTP=7

# switch s2
fvctl -f /dev/null add-flowspace http_F5 2 100 in_port=3,tp_src=8000 HTTP=7
fvctl -f /dev/null add-flowspace http_F6 2 100 in_port=3,tp_dst=8000 HTTP=7
#fvctl -f /dev/null add-flowspace http_F5 2 100 in_port=3,dl_type=0x0800,nw_proto=6,nw_src=10.0.0.6,dl_src=00:00:00:00:00:06 HTTP=7
#fvctl -f /dev/null add-flowspace http_F6 2 100 in_port=3,dl_type=0x0800,nw_proto=6,nw_dst=10.0.0.6,dl_dst=00:00:00:00:00:06 HTTP=7
#fvctl -f /dev/null add-flowspace http_F5 2 100 in_port=3,dl_type=0x0800,nw_proto=6,tp_src=8000 HTTP=7
#fvctl -f /dev/null add-flowspace http_F6 2 100 in_port=3,dl_type=0x0800,nw_proto=6,tp_dst=8000 HTTP=7
fvctl -f /dev/null add-flowspace http_F7 2 100 in_port=1 HTTP=7

# ==== Slice (ftp) ====

# switch s1
fvctl -f /dev/null add-flowspace ftp_F1 1 10 in_port=3 FTP=7
fvctl -f /dev/null add-flowspace ftp_F2 1 10 in_port=4 FTP=7
fvctl -f /dev/null add-flowspace ftp_F3 1 10 in_port=5 FTP=7
fvctl -f /dev/null add-flowspace ftp_F4 1 10 in_port=5 FTP=7

# switch s2
fvctl -f /dev/null add-flowspace ftp_F5 2 10 in_port=3 FTP=7
fvctl -f /dev/null add-flowspace ftp_F6 2 10 in_port=3 FTP=7
fvctl -f /dev/null add-flowspace ftp_F7 2 10 in_port=2 FTP=7

# Test 7:

## Objetivos:
1. Crear slices usando comandos basicos de flowVisor sobre la red sustrato mostrada pero manejando otros campos Match.
2. Mirar de dos slices coexistentes.
3. Verificar el efecto de las prioridades.

## Red sustrato:  
Esta topología conecta seis equipos por medio de dos switch. A los nodos (h1, h2, h3 y h4) conectados al switch S1 seran los clientes, mientras que los nodos (http y ftp) conectados al switch S2 funcionaran como servidores.

```
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
```


En la topologia los nodos toman tienen las siguientes caracteristicas:


|Nodo        |Funcion     |Puerto      |IP          |
|:----------:|:----------:|:----------:|:----------:|
|ftp         |servidor    |21          |10.0.0.1    |
|h1          |cliente     |            |10.0.0.2    |
|h2          |cliente     |            |10.0.0.3    |
|h3          |cliente     |            |10.0.0.4    |
|h4          |cliente     |            |10.0.0.5    |
|http        |servidor    |8000        |10.0.0.6    |


## Controlador: 
El modulo ejecutado es l2_learning.py que hace que el controlados funcione como un switch capa 2.
Archivo: l2_learning.py

Para la slice HTTP:
```
./pox.py openflow.of_01 --port=10001 forwarding.l2_learning samples.pretty_log log.level --DEBUG
```

Para la slice FTP:
```
./pox.py openflow.of_01 --port=10002 forwarding.l2_learning samples.pretty_log log.level --DEBUG
```
## Redes Virtuales: 

### Slice 1 (HTTP)

```
             H1
              |
         H2   |                 http
           \  |                / 
            \ |               /
             S1 ----------- S2
             
```

La siguiente tabla define los match de los flowspaces de la slice VN1:

|DPID        |Priority    |in_port     |dl_vlan     |dl_src      |dl_dst      |dl_type     |nw_src      |nw_dst      |nw_proto    |nw_tos      |tp_src      |tp_dst       |
|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|
|any|110|***|***|00:00:00:00:00:02|***|0x806|10.0.0.2|***|***|***|***|***|
|any|110|***|***|00:00:00:00:00:03|***|0x806|10.0.0.3|***|***|***|***|***|
|any|110|***|***|00:00:00:00:00:06|***|0x806|10.0.0.6|***|***|***|***|***|
|1|100|1|***|00:00:00:00:00:06|***|***|***|***|***|***|***|***|
|1|100|2|***|00:00:00:00:00:06|***|***|***|***|***|***|***|***|
|1|100|5|***|00:00:00:00:00:06|***|***|***|***|***|***|8000|***|
|1|100|5|***|00:00:00:00:00:06|***|***|***|***|***|***|***|8000|
|2|100|3|***|00:00:00:00:00:06|***|***|***|***|***|***|8000|***|
|2|100|3|***|00:00:00:00:00:06|***|***|***|***|***|***|***|8000|
|2|100|1|***|00:00:00:00:00:06|***|***|***|***|***|***|***|***|

### Slice 2 (FTP)

```
    
            
             S1 ----------- S2
            / |               \ 
           /  |                \
         H3   |                 ftp
              |
             H4
         
```

La siguiente tabla define los match de los flowspaces de la slice VN2:

|DPID        |Priority    |in_port     |dl_vlan     |dl_src      |dl_dst      |dl_type     |nw_src      |nw_dst      |nw_proto    |nw_tos      |tp_src      |tp_dst       |
|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|
|1|10|3|***|***|***|***|***|***|***|***|***|***|
|1|10|4|***|***|***|***|***|***|***|***|***|***|
|1|10|5|***|***|***|***|***|***|***|***|***|***|
|2|10|3|***|***|***|***|***|***|***|***|***|***|
|2|10|2|***|***|***|***|***|***|***|***|***|***|

## Pruebas realizadas:

### Habilitando solo una slice:

## Run log (comandos ejecutados):

```
# Consola 1 (mininet)
sudo mn --custom topo_test4.py --topo topo_test4 --link tc --controller remote --mac --arp
pingall
xterm h1 h2 h3 h4 http ftp

# Consola 2 (Controlador POX - Slice HTTP)
./pox.py openflow.of_01 --port=10001 forwarding.l2_learning samples.pretty_log log.level --DEBUG

# Consola 3 (Controlador POX - Slice FTP)
./pox.py openflow.of_01 --port=10002 forwarding.l2_learning samples.pretty_log log.level --DEBUG

# Consola 4 (flowvisor)
# La primera vez se debe arrancar Flowvisor
sudo /etc/init.d/flowvisor start

sh fv_test7.sh
fvctl -f /dev/null list-slices
fvctl -f /dev/null list-slice-info HTTP
fvctl -f /dev/null list-slice-info FTP
fvctl -f /dev/null list-datapath-info 1
fvctl -f /dev/null list-datapath-info 2
fvctl -f /dev/null list-flowspace -s HTTP
fvctl -f /dev/null list-flowspace -s FTP

# Consola xterm http
cd webserver
python -m SimpleHTTPServer

# Consola xterm ftp
cd ftpserver
python ftpserver.py

# Consola xterm h1
curl http://10.0.0.6:8000
ftp 10.0.0.1

# Consola xterm h2
curl http://10.0.0.6:8000
ftp 10.0.0.1

# Consola xterm h3
curl http://10.0.0.6:8000
ftp 10.0.0.1

# Consola xterm h4
curl http://10.0.0.6:8000
ftp 10.0.0.1

# Medicion del ancho de banda

# Consola xterm http
Se da de baja el servicio web --> CTRL + C
iperf -s -p 8000 &

# Consola xterm ftp
Se da de baja el servicio ftp --> CTRL + C
iperf -s -p 21 &

# Medicion de ancho de banda desde los clientes (no simultaneo)

# Consola xterm h1
iperf -c 10.0.0.6 -p 8000
iperf -c 10.0.0.1 -p 21

# Consola xterm h2
iperf -c 10.0.0.6 -p 8000
iperf -c 10.0.0.1 -p 21

# Consola xterm h3
iperf -c 10.0.0.6 -p 8000
iperf -c 10.0.0.1 -p 21

# Consola xterm h4
iperf -c 10.0.0.6 -p 8000
iperf -c 10.0.0.1 -p 21

# Medicion de ancho de banda desde los clientes (simultaneo)

# Consola xterm h1
iperf -c 10.0.0.6 -p 8000

# Consola xterm h4
iperf -c 10.0.0.1 -p 21

```

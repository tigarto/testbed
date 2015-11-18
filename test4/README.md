# Test 4:

## Objetivos:
1. Crear slices usando comandos basicos de flowVisor sobre la red sustrato mostrada.
2. Mirar de dos slices coexistentes cuando estas comparten recursos como los puertos.
3. Verificar el efecto de las prioridades.

## Red sustrato (La misma del test 1):  
Esta topología sencilla conecta tres equipos por medio de dos switch. El ancho de banda de los enlaces será de 100 Mbps. El objetivo a medida que se avance es ir virtualizando transitoriamente.

```
         H1
           \
            \
             S1 ----------- S2 ----- H3
            /
           /
         H2
```

## Controlador: 
El modulo ejecutado es hub.py el cual hace que el controlador funciones como hub.
Archivo: hub.py

Para la slice VN1:
```
./pox.py openflow.of_01 --port=10001 forwarding.hub
```

Para la slice VN2:
```
./pox.py openflow.of_01 --port=10002 forwarding.hub
```
## Redes Virtuales: 

### Slice 1 (VN1)

```
         H1
           \
            \
             S1 ----------- S2 ----- H3

```

La siguiente tabla define los match de los flowspaces de la slice VN1:

|DPID        |Priority    |in_port     |dl_vlan     |dl_src      |dl_dst      |dl_type     |nw_src      |nw_dst      |nw_proto    |nw_tos      |tp_src      |tp_dst       |
|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|
|1|1|2|***|***|***|***|***|***|***|***|***|***|
|1|1|1|***|***|***|***|***|***|***|***|***|***|
|2|1|any|***|***|***|***|***|***|***|***|***|***|

### Slice 2 (VN2)

```
    
            
             S1 ----------- S2 ----- H3
            /
           /
         H2
         
```

La siguiente tabla define los match de los flowspaces de la slice VN1:

|DPID        |Priority    |in_port     |dl_vlan     |dl_src      |dl_dst      |dl_type     |nw_src      |nw_dst      |nw_proto    |nw_tos      |tp_src      |tp_dst       |
|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|
|1|1|3|***|***|***|***|***|***|***|***|***|***|
|1|1|1|***|***|***|***|***|***|***|***|***|***|
|2|1|any|***|***|***|***|***|***|***|***|***|***|

## Pruebas realizadas:

### Habilitando solo una slice:

1. Solo VN1 habilitada

```
fvctl -f /dev/null update-slice --disable-slice VN2
fvctl -f /dev/null list-slices
```

2. Solo VN2 habilitada

Teniendo en cuenta el estado anterior de las slices se habilita VN2 y se deshabilita VN1

```
fvctl -f /dev/null update-slice --enable-slice VN2
fvctl -f /dev/null update-slice --disable-slice VN1
fvctl -f /dev/null list-slices
```

3. Ambas slices habilitadas

Se habilita VN1 pues VN2 ya se encuentra habilitada desde caso anterior

```
fvctl -f /dev/null update-slice --enable-slice VN1
fvctl -f /dev/null list-slices
```

4. Cambio de la prioridad de los flowspaces de la slice VN2
La prioridad de los slices de ambas slices es la misma (1) por lo que se procedera a cambiar la a cambiar los flowspaces para la slice VN2 por una prioridad mas alta.
La tabla de Flowspaces quedara asi:

Para la slice VN1:

|DPID        |Priority    |in_port     |dl_vlan     |dl_src      |dl_dst      |dl_type     |nw_src      |nw_dst      |nw_proto    |nw_tos      |tp_src      |tp_dst       |
|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|
|1|1|2|***|***|***|***|***|***|***|***|***|***|
|1|1|1|***|***|***|***|***|***|***|***|***|***|
|2|1|any|***|***|***|***|***|***|***|***|***|***|

Para la slice VN2:

|DPID        |Priority    |in_port     |dl_vlan     |dl_src      |dl_dst      |dl_type     |nw_src      |nw_dst      |nw_proto    |nw_tos      |tp_src      |tp_dst       |
|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|
|1|10|3|***|***|***|***|***|***|***|***|***|***|
|1|10|1|***|***|***|***|***|***|***|***|***|***|
|2|10|any|***|***|***|***|***|***|***|***|***|***|


### Flowvisor (fvctl)
Comandos ejecutados con el flowvisor
```
# Caso igual prioridad
sh fv_test4_1.sh

# Caso diferte prioridad
sh fv_test4_2.sh


# Verificando las caracteristicas de las slices (Comandos flowvisor aplicados)
fvctl -f /dev/null list-slices
fvctl -f /dev/null list-slice-info VN1
fvctl -f /dev/null list-slice-info VN2
fvctl -f /dev/null list-datapath-info 1
fvctl -f /dev/null list-datapath-info 2
fvctl -f /dev/null list-flowspace -s VN1
fvctl -f /dev/null list-flowspace -s VN2
```

### pingall
Para verificar conectividad entre todos los nodos de la red

```
pingall
```

### iperf
En la topologia los nodos toman las siguientes funcionalidades:


|Nodo        |Funcion     |Puerto      |IP          |
|:----------:|:----------:|:----------:|:----------:|
|h1          |cliente     |4000        |10.0.0.1    |
|h2          |cliente     |5000        |10.0.0.2    |
|h3          |servidor    |4000 - 5000 |10.0.0.3    |

Se Comandos ejecutados

```
# En h3
iperf -s -p 4000 &
iperf -s -p 5000 &

# En h1
iperf -c 10.0.0.3 -p 4000

# En h2
iperf -c 10.0.0.3 -p 5000

```

## Run log (comandos ejecutados):
```
# Consola 1 (mininet)
sudo mn --custom topo_test4.py --topo topo_test4 --link tc --controller remote --mac --arp
pingall
xterm h1 h2 h3

# Consola 2 (Controlador POX)
./pox.py openflow.of_01 --port=10001 forwarding.hub

# Consola 3 (Controlador POX)
./pox.py openflow.of_01 --port=10002 forwarding.hub

# Consola 4 (h3)
iperf -s 4000 &
iperf -s 5000 &

# Consola 5 (h1)
iperf -c 10.0.0.3 -p 4000

# Consola 6 (h2)
iperf -c 10.0.0.3 -p 5000
```

# Test 2

## Red sustrato (La misma empleada en el test 1):  
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

## Redes Virtuales: 
No hay

## Pruebas realizadas:
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

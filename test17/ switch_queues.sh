
# switch 1
echo "Configurando colas del switch 1"
sudo ovs-vsctl set port s1-eth3 qos=@newqos \
-- --id=@newqos create qos type=linux-htb \
other-config:max-rate=100000000 queues=0=@q0,1=@q1,2=@q2 \
-- --id=@q0 create queue other-config:min-rate=100000000 other-config:max-rate=100000000 \
-- --id=@q1 create queue other-config:min-rate=20000000 other-config:max-rate=20000000 \
-- --id=@q2 create queue other-config:min-rate=80000000 other-config:max-rate=80000000

# switch 2
echo "Configurando colas del switch 2"
sudo ovs-vsctl set port s2-eth1 qos=@newqos \
-- --id=@newqos create qos type=linux-htb \
other-config:max-rate=100000000 queues=0=@q0,1=@q1,2=@q2 \
-- --id=@q0 create queue other-config:min-rate=100000000 other-config:max-rate=100000000 \
-- --id=@q1 create queue other-config:min-rate=20000000 other-config:max-rate=20000000 \
-- --id=@q2 create queue other-config:min-rate=80000000 other-config:max-rate=80000000

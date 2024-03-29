#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from topology_project import NetworkTopo
from mininet.link import Intf


def run():
    
    # STEP 1: Create the network using mininet
    topo = NetworkTopo()
    net = Mininet(topo=topo)
    net.staticArp()

    # Add routing for reaching networks that aren't directly connected
    net['r1'].cmd('sysctl net.ipv4.ip_forward=1')
    net['r2'].cmd('sysctl net.ipv4.ip_forward=1')
    net['r3'].cmd('sysctl net.ipv4.ip_forward=1')
    info(net['r1'].cmd("ip route add 10.0.1.0/24 via 10.0.2.2 dev r1-eth2"))
    info(net['r1'].cmd("ip route add 192.168.0.0/24 via 10.0.2.2 dev r1-eth2"))
    info(net['r2'].cmd("ip route add 10.0.0.0/24 via 10.0.2.1 dev r2-eth2"))
    info(net['r2'].cmd("ip route add 10.0.1.0/24 via 10.0.3.2 dev r2-eth1"))
    info(net['r3'].cmd("ip route add 10.0.0.0/24 via 10.0.3.1 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 192.168.0.0/24 via 10.0.3.1 dev r3-eth2"))
    
    # STEP 2: Add firewall on router1 to implemend rules on host3 and host4
    net['r1'].cmd("iptables -A FORWARD -s 10.0.1.2 -d 10.0.0.3 -j ACCEPT")
    net['r1'].cmd("iptables -A FORWARD -s 10.0.1.3 -d 10.0.0.3 -j ACCEPT")
    net['r1'].cmd("iptables -A FORWARD -s 10.0.1.4 -d 10.0.0.3 -j ACCEPT")
    net['r1'].cmd("iptables -A FORWARD -d 10.0.0.3 -j DROP")
    
    net['r1'].cmd("iptables -A FORWARD -s 192.168.0.2 -d 10.0.0.4 -j ACCEPT")
    net['r1'].cmd("iptables -A FORWARD -s 192.168.0.6 -d 10.0.0.4 -j ACCEPT")
    net['r1'].cmd("iptables -A FORWARD -s 192.168.0.7 -d 10.0.0.4 -j ACCEPT")
    net['r1'].cmd("iptables -A FORWARD -d 10.0.0.4 -j DROP")
    
    # STEP 3: Create an HTTP server on host6 
    net['h6'].cmd("python -m http.server 80 &")
    
    # Protect h6, h7 from port scanning
    net['r2'].cmd("iptables -A FORWARD -d 192.168.0.7,192.168.0.6 -p tcp --tcp-flags ALL SYN -j DROP")
    net['r2'].cmd("iptables -A FORWARD -d 192.168.0.7,192.168.0.6  -p tcp --tcp-flags ALL FIN -j DROP")
    net['r2'].cmd("iptables -A FORWARD -d 192.168.0.7,192.168.0.6  -p tcp --tcp-flags ALL NONE-j DROP")
    net['r2'].cmd("iptables -A FORWARD -d 192.168.0.7,192.168.0.6  -p tcp --tcp-flags ALL URG,PSH,FIN -j DROP")
    net['r2'].cmd("iptables -A FORWARD -d 192.168.0.7,192.168.0.6  -p tcp --tcp-flags ALL ACK -j DROP")
    
    # Protect h3 from port scanning
    net['r2'].cmd("iptables -A FORWARD -d 10.0.0.3 -p tcp --tcp-flags ALL SYN -j DROP")
    net['r2'].cmd("iptables -A FORWARD -d 10.0.0.3 -p tcp --tcp-flags ALL FIN -j DROP")
    net['r2'].cmd("iptables -A FORWARD -d 10.0.0.3 -p tcp --tcp-flags ALL NONE-j DROP")
    net['r2'].cmd("iptables -A FORWARD -d 10.0.0.3 -p tcp --tcp-flags ALL URG,PSH,FIN -j DROP")
    net['r2'].cmd("iptables -A FORWARD -d 10.0.0.3 -p tcp --tcp-flags ALL ACK -j DROP")
    
    # STEP 4: Open ports 25, 43 and 502 on host7
    net['h7'].cmd("python3 port.py 25 &")
    net['h7'].cmd("python3 port.py 43 &")
    net['h7'].cmd("python3 port.py 502 &")
    
    # STEP a-b: Execute server and client files on hosts 3 and 2
    net['h3'].cmd("python3 server.py &")
    net['h2'].cmd("python3 client.py &")
    
    # Deactivate ipv6 ips
    net['ips'].cmd('sysctl -w net.ipv6.conf.all.disable_ipv6=1')
    net['ips'].cmd('sysctl -w net.ipv6.conf.default.disable_ipv6=1')
    net['ips'].cmd('sysctl -w net.ipv6.conf.lo.disable_ipv6=1')
    
    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()

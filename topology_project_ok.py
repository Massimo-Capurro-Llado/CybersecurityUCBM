from mininet.topo import Topo
from mininet.link import Intf
from mininet.cli import CLI




class NetworkTopo(Topo):
    def build(self, **_opts):

        # Add 3 routers in two different subnets
        r1 = self.addHost('r1', ip='10.0.0.1/24')
        r2 = self.addHost('r2', ip='192.168.0.1/24')
        r3 = self.addHost('r3', ip='10.0.1.1/24')

        # Add 3 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        
        # Add ips
        ips = self.addHost('ips', ip = '0,0,0,0', netmask = '0,0,0,0')
        
        # Add host-switch links in the same subnet
        self.addLink(s1, r1)

        self.addLink(s2, r2)
                     
        self.addLink(s3, r3)

        # Add router-router link in a new subnet for the router-router connection
        self.addLink(r1,
                     r2,
                     intfName1='r1-eth2',
                     intfName2='r2-eth2',
                     params1={'ip': '10.0.2.1/24'},
                     params2={'ip': '10.0.2.2/24'})
        
        self.addLink(r2,
                     r3,
                     intfName1='r2-eth1',
                     intfName2='r3-eth2',
                     params1={'ip': '10.0.3.1/24'},
                     params2={'ip': '10.0.3.2/24'})
        
        
         # Adding hosts specifying the default route
        h1 = self.addHost(name='h1',
                          ip='10.0.0.5/24',
                          defaultRoute='via 10.0.0.1')
        h2 = self.addHost(name='h2',
                          ip='10.0.0.2/24',
                          defaultRoute='via 10.0.0.1')
        h3 = self.addHost(name='h3',
                          ip='10.0.0.3/24',
                          defaultRoute='via 10.0.0.1')
        h4 = self.addHost(name='h4',
                          ip='10.0.0.4/24',
                          defaultRoute='via 10.0.0.1')
        h5 = self.addHost(name='h5',
                          ip='192.168.0.2/24',
                          defaultRoute='via 192.168.0.1')
        h6 = self.addHost(name='h6',
                          ip='192.168.0.6/24',
                          defaultRoute='via 192.168.0.1')
        h7 = self.addHost(name='h7',
                          ip='192.168.0.7/24',
                          defaultRoute='via 192.168.0.1')
        h8 = self.addHost(name='h8',
                          ip='10.0.1.4/24',
                          defaultRoute='via 10.0.1.1')
        h9 = self.addHost(name='h9',
                          ip='10.0.1.3/24',
                          defaultRoute='via 10.0.1.1')
        h10 = self.addHost(name='h10',
                          ip='10.0.1.2/24',
                          defaultRoute='via 10.0.1.1')      

        # Add host-switch links
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)
        self.addLink(h5, s2)
        self.addLink(h7, s2)
        self.addLink(h8, s3)
        self.addLink(h9, s3)
        self.addLink(h10,s3)
        
         # Add ips links
        self.addLink(s2, ips)
        self.addLink(h6, ips)
        


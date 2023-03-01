from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.cli import CLI

net = Mininet(controller=Controller, switch=OVSKernelSwitch)

controller = net.addController('c0')

switch = net.addSwitch('s1')

h1 = net.addHost('h1')
h2 = net.addHost('h2')

net.start()


switch.start([controller])

h1.cmd('ping -c 3 h2')

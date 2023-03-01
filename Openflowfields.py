from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.link import TCLink

def start_network():
    # Create Mininet network
    net = Mininet(controller=Controller, switch=OVSSwitch, link=TCLink)
    
    
    # Add hosts, switch, controller and links to network
    controller = net.addController('c0')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    s1 = net.addSwitch('s1')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    
    # Start network and assign IP addresses to hosts
    net.start()
    switch.start([controller])
    
    h1.cmd('ifconfig h1-eth0 10.0.0.1 netmask 255.255.255.0')
    h2.cmd('ifconfig h2-eth0 10.0.0.2 netmask 255.255.255.0')
    
    # Define 25 OpenFlow header fields on controller using ovs-ofctl command
    fields = [
        "in_port",
        "in_phy_port",
        "metadata",
        "eth_dst",
        "eth_src",
        "eth_type",
        "vlan_vid",
        "vlan_pcp",
        "ip_dscp",
        "ip_ecn",
        "ip_proto",
        "ipv4_src",
        "ipv4_dst",
        "tcp_src",
        "tcp_dst",
        "udp_src",
        "udp_dst",
        "sctp_src",
        "sctp_dst",
        "icmpv4_type",
        "icmpv4_code",
        "arp_op",
        "arp_spa",
        "arp_tpa",
        "arp_sha",
        "arp_tha"
    ]
    for field in fields:
        net.controllers[0].cmd(f'ovs-ofctl add-flow s1 {field},actions=output:2')
    
    # Dump OpenFlow flows and display 25 header fields
    flows = net.controllers[0].cmd('ovs-ofctl dump-flows s1')
    print(flows)
    
    # Stop network
    net.stop()

if __name__ == '__main__':
    start_network()


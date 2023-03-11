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
    s1.start([controller])
    
    h1.cmd('ifconfig h1-eth0 10.0.0.1 netmask 255.255.255.0')
    h2.cmd('ifconfig h2-eth0 10.0.0.2 netmask 255.255.255.0')
    
    # Define flow rules for all available header fields in OVS 2.9.8 and OpenFlow 1.5
    """fields = {
        'in_port': 1,
        'in_phy_port': 1,
        'metadata': 0x1234567890abcdef,
        'dl_src': '00:00:00:00:00:01',
        'dl_dst': '00:00:00:00:00:02',
        'dl_vlan': 4096,
        'dl_vlan_pcp': 3,
        'dl_type': 2048,
        'nw_src': '10.0.0.1',
        'nw_dst': '10.0.0.2',
        'nw_proto': 6,
        'nw_tos': 10,
        'tp_src': 1234,
        'tp_dst': 80,
        'icmp_type': 8,
        'icmp_code': 0,
        'arp_op': 1,
        'arp_spa': '10.0.0.1',
        'arp_tpa': '10.0.0.2',
        'arp_sha': '00:00:00:00:00:01',
        'arp_tha': '00:00:00:00:00:00',
        'ipv6_src': '2001:db8::1',
        'ipv6_dst': '2001:db8::2',
        'ipv6_flabel': 1234,
        'icmpv6_type': 128,
        'icmpv6_code': 0,
        'ipv6_nd_target': '2001:db8::1',
        'ipv6_nd_sll': '00:00:00:00:00:01',
        'ipv6_nd_tll': '00:00:00:00:00:00'
    }"""
   
    net.controllers[0].cmd("ovs-ofctl add-flow s1 in_port=1,actions=NORMAL")
    net.controllers[0].cmd("ovs-ofctl add-flow s1 in_phy_port=1,actions=NORMAL")
    net.controllers[0].cmd("ovs-ofctl add-flow s1 metadata=0x1234567890abcdef,actions=NORMAL")
    net.controllers[0].cmd("ovs-ofctl add-flow s1 dl_src=00:00:00:00:00:01,actions=NORMAL")
    net.controllers[0].cmd("ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:02,actions=NORMAL")
    net.controllers[0].cmd("ovs-ofctl add-flow s1 dl_vlan=4096,actions=NORMAL")
    net.controllers[0].cmd("ovs-ofctl add-flow s1 dl_vlan_pcp=3,actions=NORMAL")
    net.controllers[0].cmd("ovs-ofctl add-flow s1 dl_type=2048,actions=NORMAL")
    net.controllers[0].cmd("ovs-ofctl add-flow s1 nw_src=10.0.0.1,actions=NORMAL")
    net.controllers[0].cmd("ovs-ofctl add-flow s1 nw_dst=10.0.0.2,actions=NORMAL")
    net.controllers[0].cmd("ovs-ofctl add-flow s1 nw_proto=6,actions=NORMAL")
    net.controllers[0].cmd("ovs-ofctl add-flow s1 nnw_tos=10,actions=NORMAL")
    
    


    # Dump OpenFlow flows and display 25 header fields
    flows = net.controllers[0].cmd('ovs-ofctl dump-flows s1')
    print(flows)
    
    # Stop network
    net.stop()

if __name__ == '__main__':
    start_network()


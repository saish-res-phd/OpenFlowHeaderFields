from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.link import TCLink
import itertools

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
    
    
    fields = {
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
    }
    combinations = []
    for i in range(len(fields) + 1):
      for combo in itertools.combinations(fields.items(), i):
        combination = dict(combo)
        match_str = ",".join(["{}={}".format(k, v) for k, v in combination.items()])
        combinations.append(match_str)
       
    for match_str in combinations:
      net.controllers[0].cmd("ovs-ofctl add-flow s1 {},actions=NORMAL".format(match_str))
      
    # Dump OpenFlow flows and display all header fields
    flows = net.controllers[0].cmd("ovs-ofctl dump-flows s1")
    for flow in flows.splitlines():
        print(flow)
        net.controllers[0].cmd("ovs-ofctl --protocols=OpenFlow13 match s1 {}".format(flow.split(" cookie")[0]))
    # Stop network
    #net.stop()
    
if __name__ == '__main__':
    start_network()
